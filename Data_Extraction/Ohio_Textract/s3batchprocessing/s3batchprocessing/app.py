'''
Amazon S3 Batch Program to run on Ohio PDFs to send files to SQS queue. 
'''

# Handle imports
import json
import logging
from pythonlogging import jsonlogger
import boto3
import os

# Set up constants
SQS = boto3.client('sqs')
QUEUE = 'S3_batch_pdf_to_queue'


# Set up logging
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)


# Send SQS Message
def send_sqs_message(msg):
    ''' 
    Sends sqs
    '''
    pass
# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    LOG.info("event: {}".format(event))

    request = {}

    # Parse job parameters
    # request["jobId"] = event['job']['id']
    # request["invocationId"] = event['invocationId']
    # request["invocationSchemaVersion"] = event['invocationSchemaVersion']

    # Task
    # request["task"] = event['tasks'][0]
    # request["taskId"] = event['tasks'][0]['taskId']
    # request["objectName"] = urllib.parse.unquote_plus(event['tasks'][0]['s3Key'])
    # request["s3VersionId"] = event['tasks'][0]['s3VersionId']
    # request["s3BucketArn"] = event['tasks'][0]['s3BucketArn']
    # request["bucketName"] = request["s3BucketArn"].split(':')[-1]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Completed Batch Job",
            # "location": ip.text.replace("\n", "")
        }),
    }
