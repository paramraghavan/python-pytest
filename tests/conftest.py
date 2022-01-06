"""Shared fixtures."""

import pytest

# import sys
# # This is needed so Python can find test_tools on the path.
# sys.path.append('../..')

from addressbook import Addressbook


@pytest.fixture
def addressbook(tmpdir):
    """Provides an empty Addressbook"""
    return Addressbook(tmpdir)

'''
aws fixtures
'''

import os
import boto3


@pytest.fixture()
def set_envvars():
    """ Sets environment variables"""
    def _set_envvars(requried_envvars, envvar_overrides=None):
        for envar in requried_envvars:
            env_value = f'test-{envar}'
            os.environ[envar] = env_value

        if envvar_overrides:
            for override_envar in envvar_overrides:
                os.environ[override_envar] = envvar_overrides[override_envar]

    return _set_envvars


# KeySchema = [
#                 {
#                     'AttributeName': 'datasource',
#                     'KeyType': 'HASH'
#                 },
#                 {
#                     'AttributeName': 'partitionkey',
#                     'KeyType': 'RANGE'
#                 }
#             ],
# AttributeDefinitions = [
#                            {
#                                'AttributeName': 'datasource',
#                                'AttributeType': 'S'
#                            },
#                            {
#                                'AttributeName': 'partitionkey',
#                                'AttributeType': 'S'
#                            },
#                        ],

@pytest.fixture()
def create_dynamo_db_table():
    ''' Creates dynamodb table'''
    def _create_dynamo_db_table(table_name, key_schema, attribute_definations):
        dynamodb = boto3.resource('dynamodb', 'us-east-1')

        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definations,
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

    return _create_dynamo_db_table


from moto import mock_s3, mock_batch

@pytest.fixture
def s3():
    """Pytest fixture to be used to perfom s3 action onto
     fake moto AWS account

    Yields a fake boto3 batch client
    """
    with mock_s3():
        s3 = boto3.client("s3")
        yield s3


@pytest.fixture
def batch():
    """Pytest fixture to be used to perform batch action onto
     fake moto AWS account

    Yields a fake boto3 batch client
    """
    with mock_batch():
        batch = boto3.client("batch")
        yield batch

from botocore.stub import Stubber
@pytest.fixture()
def batch_stub_(batch):
    boto3.setup_default_session(region_name="us-east-1")
    # batch_client = boto3.client('batch')
    with Stubber(batch) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture()
def create_s3_bucket():
    ''' Creates s3 bucket.'''
    def _create_s3_bucket(bucket_name):
        s3 = boto3.resource('s3', 'us-east-1')
        s3.create_bucket(Bucket=bucket_name)

    return _create_s3_bucket


@pytest.fixture()
def s3_put_object_metadata():
    ''' Add metadata to S3'''
    def _s3_put_object_metadata(bucket_name, s3key, file_content_str, metadata):
        s3_client = boto3.client('s3', 'us-east-1')
        s3_client.put_object(Body=file_content_str.encode(), Bucket=bucket_name, Key=s3key, Metadata=metadata)

    return _s3_put_object_metadata


@pytest.fixture()
def read_item_from_dynamodb():
    ''' Read item/record from dynamodb.'''
    def _read_item_from_dynamodb(source_table, key):
        dynamodb_resource = boto3.resource("dynamodb", region_name='us-east-1')
        dynamodb_tbl = dynamodb_resource.Table(source_table)

        response = dynamodb_tbl.get_item(
            TableName=source_table,
            Key=key
        )
        return response['Item']

    return _read_item_from_dynamodb

