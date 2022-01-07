
import time
import boto3
import os
import ast
import pytest
from pytest_mock import mocker
from moto import mock_batch, mock_iam, mock_ec2
from botocore.client import BaseClient
from aws.utils.boto3_utils import describe_batch_jobs
from pytest_mock import mocker
import docker

# marker used by code to identify if the module is being exercised by pytest
os.environ["PYTEST_CURRENT_TEST"] = 'yes'

from aws.check_batchjob_status import lambda_function
from aws.check_batchjob_status.lambda_function import get_batch
from aws.utils.boto3_utils import retry_exception_list

import copy

'''
https://adamj.eu/tech/2019/04/22/testing-boto3-with-pytest-fixtures/
'''
import pytest
from botocore.stub import Stubber

'''
Note in the case of stubber the boto3 batch client handle is shared b/w the tested module and the testing
module. The stubs the shared client handle, so the same stubbed instance is used by the tested module
in our case see import
from aws.check_batchjob_status.lambda_function import batch_client

'''
@pytest.fixture()
def batch_stub():
    boto3.setup_default_session(region_name="us-east-1")
    # batch_client = boto3.client('batch')
    with Stubber(get_batch()) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()

@mock_batch
def test_lambda_handler(mocker, batch_stub):

    input_event = \
        {
            "batchjobid": "x9e393xb-266f-43e6-9682-600283cedc91"
        }

    response = {
        "jobs": [
            {
                "jobName": "job_name",
                "jobId": "job_id",
                "jobQueue": "job_queue",
                "startedAt": 123,
                "jobDefinition": "foobar",
                "status": "",
            }
        ]
    }

    for i in range(3):
        if i == 2:
            response = response.copy()
            response = copy.deepcopy(response)
            response["jobs"][0]["status"] = "SUCCEEDED" # 3rd time success
            print("Adding response: ", response)
            batch_stub.add_response("describe_jobs", response)
        else:
            batch_stub.add_client_error("describe_jobs", service_error_code=retry_exception_list[i],service_message='', http_status_code=400)

    actual_response = lambda_function.lambda_handler(input_event, "")
    assert actual_response['batchJobStatus']['statusCode'] == 0