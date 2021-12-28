import time
import boto3
import os
import ast
import os
if "PYTEST_CURRENT_TEST" in os.environ:
# We are running under pytest, act accordingly...
    from aws.utils import boto3_utils
else:
    # this is for the serverless deploy to work, serverless.yml has to be in asw and cannot be src folder with the current setup
    from utils import boto3_utils

def lambda_handler(event, context):
    print('Incoming sns request {0}'.format(repr(event)))
    sns_msg = event["Records"][0]["Sns"]
    print(f'sns message: {sns_msg} ')
    message_attributes = sns_msg["MessageAttributes"]
    print(f'message_attributes: {message_attributes} ')
    producer_datasource = event["Records"][0]["Sns"]["MessageAttributes"]["AnnualSurveryDatasource"]["Value"]
    print(f'producer_datasource: {producer_datasource}')
    bucket_name = producer_datasource.split('/')[0]
    print(f"bucket: {bucket_name}")
    key = producer_datasource.split('/', 1)[1:][0]
    print(f"key: {key}")

    # read the s3 object and count the number for lines including the header
    actual_record_count = boto3_utils.s3_file_line_count(bucket_name, key)
    print(f'row count{actual_record_count}')

    # read from S3 metadata --> x-amz-meta-record-count
    record_count_from_metadata = boto3_utils.read_s3_object_metadata(bucket_name, key)
    count_match = False

    if actual_record_count == record_count_from_metadata:
        count_match = True

    # on count match continue, else raise EMM alert


    # save this producer datasource to dynamodb
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    PRODUCER_INTERFACE_TABLE = os.environ['PRODUCER_INTERFACE_TABLE']
    dynamodb_table = dynamodb.Table(PRODUCER_INTERFACE_TABLE)
    partition_key = time.strftime("%Y-%m-%d")
    datalocation = f's3://{bucket_name}/{key}'
    item_key = {
        'producer_datasource': producer_datasource,
        'partition_key': partition_key
    }

    update_expr = "SET actual_record_count=:actual_record_count, record_count_from_metadata=:record_count_from_metadata, count_match_status=:count_match_status, datalocation=:dl, create_data_time=:cdt"
    expr_attr_values = {
        ':actual_record_count': actual_record_count,
        ':record_count_from_metadata': record_count_from_metadata,
        ':count_match_status': count_match,
        ':dl':datalocation,
        ':cdt': current_time
    }

    response = boto3_utils.update_dynamodb_item(dynamodb_table, item_key, update_expr, expr_attr_values)
    print('updateResponse: ' + str(response))