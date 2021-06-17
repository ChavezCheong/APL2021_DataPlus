'''
Amazon Lambda to receive SQS Queue and send document to be processed by Textract 
'''

# Handle imports
import json
import logging
import boto3
import botocore
import os
import urllib
import time

# Set up constants
QUEUE = 'S3_batch_pdf_to_queue'
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/294491488031/S3_batch_pdf_to_queue"
SNS_TOPIC = "arn:aws:sns:us-east-1:294491488031:get-textract-responses"
SNS_ROLE = "arn:aws:iam::294491488031:role/textract-service-role"

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

def start_textract_job(pdf, bucket):
    '''
    Gets message from SQS queue and sends it to Textract to start processing.
    Will get a job ID and return and also send the job to an SNS topic.
    '''
    
    # Setting up Textract Client
    LOG.info(f"Setting up Textract Client")
    TEXTRACT = boto3.client('textract')
    LOG.info(f"Successfully set up Textract Client")
    
    # Loading documents into Textract
    try:
        LOG.info(f"Detecting text for {pdf}")
        response = TEXTRACT.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': pdf
                }
            },
            NotificationChannel={
                'SNSTopicArn': SNS_TOPIC,
                'RoleArn': SNS_ROLE
            }
        )
        LOG.info(f"Text_detection for {pdf} done. \n Response: {response}")
    except Exception as error:
        raise error
    
    # Return the response
    jobId = response['JobId']
    LOG.info(f"JobId:{jobId}")
    
    
def lambda_handler(event, context):
    '''
    Lambda Entry
    '''
    
    # Keep track of total transactions
    total_count = 0
    succeeded_count = 0
    
    #LOG.info(f'Processing job, event {event}, context {context}')
    
    for record in event['Records']:
        total_count += 1
        
        # Load json record
        msg = json.loads(record['body'])
        LOG.info(msg)
        pdf = msg['pdfName']
        bucket = msg['bucketName']
        LOG.info(f"Loaded file: {pdf} that came from bucket: {bucket}")
        receipt_handle = record['receiptHandle']
        
        # Try to process message
        try:
            LOG.info(f"Attempting to start processing file: {pdf} from bucket: {bucket}")
            start_textract_job(pdf, bucket)
            LOG.info(f"Successfully processed file: {pdf} from bucket: {bucket}")
            succeeded_count += 1
            # Try to delete message
            try:
                response = delete_sqs_message(receipt_handle)
                LOG.info(f"Successfully deleted SQS message with receipt handle: {receipt_handle} with response: {response}")
            except:
                LOG.info(f"Proceeding without deleting SQS message {receipt_handle}")
                continue
        # If Throttle Errors appear
        except Exception as error:
            LOG.exception(f"Error occurred with error {error}")
            LOG.info(f"Waiting for a few seconds for queue to reset")
            time.sleep(5)
            # Reset message so lambda can pick it up again
            change_visibility(receipt_handle)
            continue
        
        
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{succeeded_count} jobs successful out of {total_count} jobs",
            # "location": ip.text.replace("\n", "")
        }),
        }