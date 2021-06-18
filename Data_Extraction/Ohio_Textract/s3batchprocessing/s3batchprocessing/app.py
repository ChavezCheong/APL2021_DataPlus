'''
Amazon S3 Batch Program to run on Ohio PDFs to send files to SQS queue. 
'''

# Handle imports
import json
import logging
import boto3
from botocore.client import Config
import os
import urllib

# Set up configurations
config = config = Config(
            retries = dict(
                max_attempts = 30
            )
        )

# Set up constants
SQS = boto3.client('sqs',config=config)
QUEUE = 'S3_batch_pdf_to_queue'
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/294491488031/S3_batch_pdf_to_queue"

# Set up logging
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
logHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)


# Send SQS Message
def send_sqs_message(msg, delay = 0):
    ''' 
    Sends SQS message containing BucketName and PDFName
    '''
    
    # Process the message
    json_msg = json.dumps(msg)
    LOG.info(f"Message processed:{json_msg}")
    
    # Send the SQS message
    response = SQS.send_message(
        QueueUrl = QUEUE_URL,
        MessageBody = json_msg,
        DelaySeconds = delay
        )
        
    LOG.info("Submitted message to queue: {}".format(json_msg))
    return response


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

    request = {}
    request['pdfName'] = urllib.parse.unquote_plus(event['tasks'][0]['s3Key'])
    request['bucketName'] = event['tasks'][0]['s3BucketArn'].split(':')[-1]
    
    # Get handlers for exceptions
    taskId = event['tasks'][0]['taskId']
    invocationId = event['invocationId']
    invocationSchemaVersion = event['invocationSchemaVersion']
    
    # Check if PDF
    basename = os.path.basename(request["pdfName"])
    dn, dext = os.path.splitext(basename)
    ext = dext[1:]
    LOG.info(f"File extension: {ext}")
    if ext in ["pdf","PDF"]:
        response = send_sqs_message(request)
        LOG.info(response)
        results = [{
        'taskId': taskId,
        'resultCode': 'Succeeded',
        'resultString': f"{request['pdfName']} from bucket {request['bucketName']} submitted for processing."
        }]
        return {
            'invocationSchemaVersion': invocationSchemaVersion,
            'treatMissingKeysAs': 'PermanentFailure',
            'invocationId': invocationId,
            'results': results
        }
    else:
        return {
            'invocationSchemaVersion': invocationSchemaVersion,
            'treatMissingKeysAs': 'PermanentFailure',
            'invocationId': invocationId,
            'results': results
        }
