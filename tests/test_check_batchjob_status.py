
import boto3
import os
# marker used by code to identify if the module is being exercised by pytest
os.environ["PYTEST_CURRENT_TEST"] = 'yes'

from aws.check_batchjob_status import lambda_function
from aws.utils.boto3_utils import retry_exception_list

import copy

'''
https://adamj.eu/tech/2019/04/22/testing-boto3-with-pytest-fixtures/
'''
import pytest
from botocore.stub import Stubber

@pytest.fixture
def local_batch_stub(mocker, batch, batch_stub):
    with mocker.patch("aws.check_batchjob_status.lambda_function.get_batch", return_value=batch):
        yield batch_stub

#@pytest.mark.skip("WIP")
def test_lambda_handler(local_batch_stub):

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
            local_batch_stub.add_response("describe_jobs", response)
        else:
            local_batch_stub.add_client_error("describe_jobs", service_error_code=retry_exception_list[i],service_message='', http_status_code=400)
    # Activate the stubber
    with local_batch_stub:
        actual_response = lambda_function.lambda_handler(input_event, "")
        assert actual_response['batchJobStatus']['statusCode'] == 0