import os
import boto3
import traceback

if "PYTEST_CURRENT_TEST" in os.environ:
# We are running under pytest, act accordingly...
    from aws.utils import boto3_utils
else:
    # this is for the serverless deploy to work, serverless.yml has to be in asw and cannot be src folder with the current setup
    from utils import boto3_utils


batch_job_status_1 = ['RUNNING', "STARTING", "SUBMITTED", "RUNNABLE", "PENDING"]

batch_client= boto3.client('batch')
def get_batch():
    return batch_client

def lambda_handler(event, context):
    statusCode = -1 # error
    jobId = event['batchjobid']
    print(f'status check for batchjobId: {jobId}')

    try:
        response = boto3_utils.describe_batch_jobs(get_batch(), jobId)
        print(f'Response: {repr(response)}')
        # Return the jobStatus
        if response and response.get('jobs'):
            jobStatus = response['jobs'][0]['status']
            if jobStatus in batch_job_status_1 :
                statusCode = 1  # in progress
            elif jobStatus == 'SUCCEEDED':
                statusCode = 0  # success
    except Exception as e:
        print(traceback.format_exc())

    event['batchJobStatus'] = {"statusCode":statusCode}
    return event