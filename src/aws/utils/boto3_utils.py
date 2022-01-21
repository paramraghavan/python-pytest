import time
import botocore
import boto3

retry_exception_list = ["Throttling", "ThrottlingException", "ThrottledException", "RequestThrottledException",
                    "TooManyRequestsException",
                    "TransactionInProgressException", "RequestLimitExceeded",
                    "BandwidthLimitExceeded", "LimitExceededException", "RequestThrottled", "SlowDown",
                    "EC2ThrottledException"]



def update_dynamodb_item(dynamo_table,item_key,expr,expr_attr_values):
    response = dynamo_table.update_item(
        Key=item_key,
        UpdateExpression=expr,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="UPDATED_NEW"
    )
    return response

'''
API --> https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file
'''
def s3_file_line_count(bucket_name, key):
    s3 = boto3.resource('s3')
    # the file can only be created under /tmp , which is the writable file system
    # else you will get an OSError -
    # OSError: [Errno 30] Read-only file system: 'my-file.CD74E7Bd'
    filename = '/tmp/my-file'
    s3.meta.client.download_file(bucket_name, key, filename)

    line_count = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line_count +=1

    return line_count

'''
In this case the s3 file is  not downloaded
'''
def s3_file_line_count_1(bucket_name, key):
    txt_file = s3.Object(bucket_name, key).get()['Body'].read().decode(
        'utf-8').splitlines()
    line_count = 0
    for line in txt_file:
        line_count +=1

    return line_count

def read_s3_object_metadata(bucket_name, key, metadata_key='record-count'):
    # s3 = boto3.client('s3')
    # response = s3.head_object(Bucket=bucket_name, Key=key)
    # print('Response: {}'.format(response))
    #
    # print("record-count : " + response['ResponseMetadata'])

    s3_resource=boto3.resource('s3')

    bucket = s3_resource.Bucket(bucket_name)
    s3Object = bucket.Object(key=key)
    print(str(s3Object.metadata))
    value = s3Object.metadata[metadata_key]

    return int(value)



def describe_batch_jobs(batch_client, jobid, retries=3, backoff=10):
    response = None
    for attempt in range(retries):
        try:
            response = batch_client.describe_jobs(jobs=[jobid])
            break
        except botocore.exceptions.ClientError as error:
            print(f'retry number: {attempt}')
            if error.response['Error']['Code'] in retry_exception_list:
                print('API call error; backing off and retrying...')
                time.sleep(backoff)
                pass
            else:
                raise error

    return response


if __name__ == '__main__':
    bucket_name = 'sample987'
    print(f"bucket: {bucket_name}")
    key = 'input/annual-enterprise-survey-2020-financial-year-provisional.csv'
    print(f'key: {key}')
    record_count = read_s3_object_metadata(bucket_name, key)
    print(f'Record Count: {record_count}')