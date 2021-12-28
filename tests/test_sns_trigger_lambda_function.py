import time
import boto3
import os
import ast
import pytest
from pytest_mock import mocker
from moto import mock_dynamodb2, mock_s3

# marker used by code to identify if the module is being exercised by pytest
os.environ["PYTEST_CURRENT_TEST"] = 'yes'

from aws.sns_trigger_lambda import lambda_function


@mock_dynamodb2
@mock_s3
def test_sns_trigger_lambda(set_envvars, create_s3_bucket, s3_put_object_metadata, create_dynamo_db_table, read_item_from_dynamodb):

    required_envvars = ['PRODUCER_INTERFACE_TABLE', 'LifecycleEnv']
    envvar_overrides = {}
    envvar_overrides['PRODUCER_INTERFACE_TABLE'] = 'producer-interface-table'
    envvar_overrides['LifecycleEnv'] = 'dev'

    set_envvars(required_envvars, envvar_overrides)

    bucket = 'sample987'
    create_s3_bucket(bucket)
    metadata = {}
    record_count = '10'
    metadata['record-count'] = record_count
    key = 'input/annual-enterprise-survey-2020-financial-year-provisional.csv'

    datalocation = f's3://{bucket}/{key}'

    s3_object_content = \
    "line 1 \n"\
    "line 2 \n"\
    "line 3\n"\
    "line 4\n"\
    "line 5\n"\
    "line 6 \n"\
    "line 7 \n"\
    "line 8\n"\
    "line 9\n"\
    "line 10\n"

    # add a file to s3 with record-cout metadata
    s3_put_object_metadata(bucket, key, s3_object_content, metadata)

    # create mock dynamodb table
    key_schema = []
    key_schema.append({'AttributeName': 'producer_datasource', 'KeyType': 'HASH'})
    key_schema.append({'AttributeName': 'partition_key', 'KeyType': 'RANGE'})

    attribute_definations = []
    attribute_definations.append({'AttributeName': 'producer_datasource', 'AttributeType': 'S'})
    attribute_definations.append({'AttributeName': 'partition_key', 'AttributeType': 'S'})

    create_dynamo_db_table(os.environ['PRODUCER_INTERFACE_TABLE'], key_schema, attribute_definations)

    input_event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-1:687162148361:dispatch:3c1c7634-edb6-43e2-9b09-02e781a1148b', 'Sns': {'Type': 'Notification', 'MessageId': '07826c52-ed6c-5f38-a87c-3616966df04a', 'TopicArn': 'arn:aws:sns:us-east-1:687162148361:dispatch', 'Subject': 'AnnualSurveryDatasource File update.', 'Message': 'Updated AnnualSurvery data source file.', 'Timestamp': '2021-12-28T02:38:57.644Z', 'SignatureVersion': '1', 'Signature': 'gRhDfpman0zibBR4B7VKgef7mAN7L4KaC8hYXkOfs5knRmmQ+q5YIt7Z5nGFKqxZiR1RWFujioABD478ogq0zfUmJxkhVO+KtJSQvuM7+Sg82fd4q1t9pAf/zuBwqwSPKg0wABjWaI5LSjYV/A+tq/HEQ2eoZLTCQfgBWCkxQKprrqyxiHiHdE2wzPnjFnwY/a4uRYSFnO6X0p3hablKX+5XO8uqtyHD6I6OmaAd3mf9ppSGnETJO/1NSRykQBi4MWrxlKVBgB6UrHhYM0zpCpb6yFS9iVEDMKR6Ow/hjLRYP0Lg9N+kWRkxDXMTdQ0LOwqc7UnyvfFDnw8lUUFKAg==', 'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:687162148361:dispatch:3c1c7634-edb6-43e2-9b09-02e781a1148b', 'MessageAttributes': {'AnnualSurveryDatasource': {'Type': 'String', 'Value': 'sample987/input/annual-enterprise-survey-2020-financial-year-provisional.csv'}}}}]}

    # invoke the lambda
    lambda_function.lambda_handler(input_event, "")

    producer_datasource = input_event["Records"][0]["Sns"]["MessageAttributes"]["AnnualSurveryDatasource"]["Value"]
    partition_key = time.strftime("%Y-%m-%d")

    key = {}
    key['producer_datasource'] = producer_datasource
    key['partition_key'] = partition_key

    result = read_item_from_dynamodb(os.environ['PRODUCER_INTERFACE_TABLE'], key)
    assert result['actual_record_count']== 10
    assert result['datalocation'] == datalocation