'''
Author: Chavez Cheong <https://github.com/ChavezCheong>
Purpose of Script: Amazon Lambda to receive completed Textract requests, retrieve it, process it and then log it.
'''

# Handle imports
import json
import logging
import boto3
import botocore
from io import StringIO
import pandas as pd
import numpy as np
import time
import uuid
import sys

# Set up constants
QUEUE = 'queue_completed_textract_jobs'
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/294491488031/queue_completed_textract_jobs"
OUTPUT_BUCKET = "enforcement-actions"
OUTPUT_PREFIX = "Massachusetts/processed_pdfs"


# Set up logging
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
logHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)

def delete_sqs_message(receipt_handle):
    '''
    Deletes message from SQS queue.
    Returns a response message
    '''
    
    #Setting up SQS connection
    LOG.info("Setting up SQS client")
    SQS = boto3.client('sqs')
    LOG.info("Successfully set up SQS client")
    
    try:
        LOG.info(f"Attempting to delete SQS receipt handle {receipt_handle}")
        response = SQS.delete_message(QueueUrl = QUEUE_URL, ReceiptHandle = receipt_handle)
    except botocore.exceptions.ClientError as error:
        LOG.exception(f"Failed to delete SQS message {receipt_handle} with error {error}")
        raise error
    return response

def change_visibility(receipt_handle):
    '''
    Resets visibility of SQS message
    '''
    
    #Setting up SQS connection
    LOG.info("Setting up SQS client")
    SQS = boto3.client('sqs')
    LOG.info("Successfully set up SQS client")
    
    try:
        SQS.change_message_visibility(
                QueueUrl = QUEUE_URL,
                ReceiptHandle=receipt_handle,
                VisibilityTimeout=0
            )
    except Exception as error:
        LOG.exception(f"Failed to change visibility for {receipt_handle} with error: {error}")

def write_s3(df):
	"""
	Write dataframes to S3 Bucket as CSV files
	"""
	csv_buffer = StringIO()
	# Remove 6490 character threshold limit
	np.set_printoptions(threshold=sys.maxsize)
	df.to_csv(csv_buffer)
	
	# Set up S3 Client
	LOG.info("Setting up S3 Client")
	S3 = boto3.resource('s3')
	LOG.info("Successfully set up S3 Client")
	
	# Create randomized UUID
	random_id = uuid.uuid4()
	filename = f"{random_id}.csv"
	response = S3.Object(OUTPUT_BUCKET, f'{OUTPUT_PREFIX}/{filename}').put(Body=csv_buffer.getvalue())
	LOG.info(f'Result of write to bucket: {OUTPUT_BUCKET} with:\n {response}')


def get_textract_job(job_id, file_name):
    '''
    Get Textract job and returns string containing all of it
    '''
    
    # Setting up Textract Client
    LOG.info("Creating Textract Client")
    TEXTRACT = boto3.client('textract')
    
    # Retrieves Textract File
    try:
        LOG.info(f"Retrieving job with JobId: {job_id} for file: {file_name}")
        response = TEXTRACT.get_document_text_detection(JobId= job_id)
        document_text = ""
        for item in response['Blocks']:
            if item['BlockType'] == "LINE":
                document_text += item['Text'] + "\n"
        LOG.info(f"Retrived one set for file: {file_name}")
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']
            LOG.info(f"Next token: {nextToken}")
        while(nextToken):
            LOG.info("Stopping for new pages in case of throttling")
            time.sleep(5)
            response = TEXTRACT.get_document_text_detection(JobId=job_id, NextToken=nextToken)
            for item in response['Blocks']:
                if item['BlockType'] == "LINE":
                    document_text += item['Text'] + "\n"
            LOG.info(f"Retrived another set for file: {file_name}")
            nextToken = None
            if('NextToken' in response):
                nextToken = response['NextToken']
                LOG.info(f"Next token: {nextToken}")
    except Exception as error:
        raise error
    return document_text

def lambda_handler(event, context):
    '''
    Lambda Entry Point
    '''
    
    # Keep track of total transactions
    total_count = 0
    succeeded_count = 0
    failed_textract_count = 0
    
    # Prepare DataFrame for insertion of data
    column_names = ["Filename", "Text"]
    df = pd.DataFrame(columns = column_names)
    
    LOG.info(f'Processing job, event {event}, context {context}')
    
    for record in event['Records']:
        total_count += 1
        
        # Load json record
        body = json.loads(record['body'])
        msg = json.loads(body['Message'])
        receipt_handle = record['receiptHandle']
        JobId = msg['JobId']
        file_name = msg['DocumentLocation']['S3ObjectName']
        bucket_name = msg['DocumentLocation']['S3Bucket']
        status = msg['Status']
        
        # Check if Textract was successful
        if status == "SUCCEEDED":
            # Try to process the message   
            try:
                LOG.info(f"Attempting to start processing file: {file_name} from bucket {bucket_name} with jobID: {JobId}")
                text = get_textract_job(JobId, file_name)
                LOG.info(f"Successfully extracted text from file: {file_name}")
                modified_file_name = file_name.split('/')[-1].split('.')[0]
                LOG.info(f"Modified file name is {modified_file_name}")
                df2 = {'Filename': modified_file_name, 'Text': text}
                df = df.append(df2, ignore_index = True)
                LOG.info(df)
                LOG.info(f"Successfully processed file: {file_name} from bucket: {bucket_name}")
                succeeded_count += 1
                # Try to delete message
                try:
                    response = delete_sqs_message(receipt_handle)
                    LOG.info(f"Successfully deleted SQS message with receipt handle: {receipt_handle} with response: {response}")
                except:
                    LOG.info(f"Proceeding without deleting SQS message {receipt_handle}")
                continue
            # If Throttle Errors occur
            except Exception as error:
                LOG.exception(f"Error occurred with error {error}")
                LOG.info(f"Waiting for a few seconds for queue to reset")
                time.sleep (5)
                # Reset message so lambda can pick it up again
                change_visibility(receipt_handle)
                continue
        else:
            failed_textract_count += 1
            LOG.info(f"Textract Request for file: {file_name} was not successful")
            # Delete failed Textract SQS message
            try:
                response = delete_sqs_message(receipt_handle)
                LOG.info(f"Successfully deleted SQS message with receipt handle: {receipt_handle} with response: {response}")
            except:
                LOG.info(f"Proceeding without deleting SQS message {receipt_handle}")
            continue
    
    # Write the CSV to S3
    LOG.info(f"Attempting to write results to S3 Bucket")
    write_s3(df)
    LOG.info(f"{succeeded_count} jobs successful out of {total_count} jobs. \n {failed_textract_count} number of Textract jobs failed.")
