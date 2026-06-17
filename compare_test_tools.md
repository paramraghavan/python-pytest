# pytest vs moto vs botocore.stub

A comprehensive comparison of testing tools for Python AWS development, with practical examples.

## Table of Contents

- [pytest - Test Framework Foundation](#pytest---test-framework-foundation)
- [moto - Full AWS Service Mocking](#moto---full-aws-service-mocking)
- [botocore.stub - Response Stubbing](#botocorestub---response-stubbing)
- [Quick Comparison Table](#quick-comparison-table)
- [Decision Guide](#decision-guide)

---

## pytest - Test Framework Foundation

### What it is
A general-purpose Python testing framework that provides the foundation for organizing and running tests.

### Use when
- Writing any test cases
- Organizing and running tests
- Managing test fixtures and setup/teardown
- Parameterizing tests
- Grouping related tests

### Example from the codebase

```python
# conftest.py
import pytest

@pytest.fixture
def addressbook(tmpdir):
    """Provides an empty Addressbook"""
    return Addressbook(tmpdir)

@pytest.fixture
def s3():
    """Pytest fixture to perform s3 action onto fake moto AWS account"""
    with mock_s3():
        s3 = boto3.client("s3")
        yield s3
```

### Key Features
- **Fixtures**: Reusable test setup/teardown
- **Markers**: `@pytest.mark.skip`, `@pytest.mark.parametrize`
- **Assertions**: Clear, readable assertion syntax
- **Plugins**: Extensible via pytest plugins (pytest-mock, pytest-cov, etc.)

---

## moto - Full AWS Service Mocking

### What it is
Mocks entire AWS services in-memory without making actual AWS API calls.

### Use when
- Testing multiple interactions with AWS services
- Need realistic service behavior (DynamoDB queries, S3 bucket operations, etc.)
- Testing complex workflows that involve AWS
- Don't want to hit real AWS (saves costs and time)
- Integration testing

### Pros
- ✅ Mocks the complete service (not just one call)
- ✅ Full service behavior simulation (queries, filters, etc.)
- ✅ Great for integration testing
- ✅ Supports many AWS services
- ✅ Minimal code changes needed

### Cons
- ❌ Slower than stubbing
- ❌ Uses more memory
- ❌ Not all AWS services supported

### Example from the codebase

```python
# conftest.py
from moto import mock_s3, mock_batch, mock_dynamodb2
import boto3

@pytest.fixture
def s3():
    """Full S3 mocking"""
    with mock_s3():
        s3 = boto3.client("s3")
        yield s3

@pytest.fixture
def dynamodb():
    """Full DynamoDB mocking"""
    with mock_dynamodb2():
        dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
        yield dynamodb

@pytest.fixture
def batch():
    """Full Batch mocking"""
    with mock_batch():
        batch = boto3.client("batch")
        yield batch
```

### Creating a Table in moto

```python
# conftest.py
@pytest.fixture()
def create_dynamo_db_table():
    '''Creates dynamodb table'''
    def _create_dynamo_db_table(table_name, key_schema, attribute_definitions):
        dynamodb = boto3.resource('dynamodb', 'us-east-1')
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
    return _create_dynamo_db_table
```

### Supported Services
- S3 (S3, S3 Control)
- DynamoDB
- Lambda
- SNS
- SQS
- Batch
- EC2
- IAM
- KMS
- RDS
- And many more...

---

## botocore.stub - Response Stubbing

### What it is
Stubs specific API responses without mocking the entire service. Intercepts boto3 calls and returns pre-defined responses.

### Use when
- Testing specific function calls and their responses
- Need precise control over what each API call returns
- Want to test error scenarios (service errors, retries)
- Want fastest, most lightweight mocking
- Unit testing individual functions

### Pros
- ✅ Very fast (only mocks specified calls)
- ✅ Low memory overhead
- ✅ Explicit control of responses
- ✅ Great for unit testing
- ✅ Works with any AWS service
- ✅ Perfect for testing error handling

### Cons
- ❌ Must manually stub every call your code makes
- ❌ Doesn't mock entire service behavior
- ❌ More verbose than moto
- ❌ No validation of complex operations

### Example from the codebase

```python
# conftest.py
from botocore.stub import Stubber
import boto3

@pytest.fixture()
def batch_stub(batch):
    boto3.setup_default_session(region_name="us-east-1")
    with Stubber(batch) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()
```

### Testing with Error Scenarios

```python
# test_check_batchjob_status.py
import pytest
from botocore.stub import Stubber

@pytest.fixture
def local_batch_stub(mocker, batch, batch_stub):
    with mocker.patch("aws.check_batchjob_status.lambda_function.get_batch", return_value=batch):
        yield batch_stub

def test_lambda_handler(local_batch_stub):
    """Test retry logic with stubbed errors"""
    input_event = {
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

    # Stub 2 errors (ThrottlingException, ServiceUnavailable), then success
    for i in range(3):
        if i == 2:
            response_copy = copy.deepcopy(response)
            response_copy["jobs"][0]["status"] = "SUCCEEDED"  # 3rd time success
            local_batch_stub.add_response("describe_jobs", response_copy)
        else:
            # Stub specific error to test retry logic
            local_batch_stub.add_client_error(
                "describe_jobs",
                service_error_code=retry_exception_list[i],
                service_message='',
                http_status_code=400
            )

    # Activate the stubber and execute code
    with local_batch_stub:
        actual_response = lambda_function.lambda_handler(input_event, "")
        assert actual_response['batchJobStatus']['statusCode'] == 0
```

### Key Methods

```python
# Add a successful response
stubber.add_response('describe_jobs', {
    "jobs": [{"jobId": "123", "status": "SUCCEEDED"}]
})

# Add an error response
stubber.add_client_error(
    'describe_jobs',
    service_error_code='ThrottlingException',
    service_message='Rate exceeded',
    http_status_code=429
)

# Verify all stubbed responses were used
stubber.assert_no_pending_responses()
```

---

## Quick Comparison Table

| Feature | pytest | moto | botocore.stub |
|---------|--------|------|---------------|
| **Purpose** | Test framework | Mock full AWS services | Stub specific responses |
| **Speed** | N/A | Medium | Fast ⚡ |
| **Memory Usage** | N/A | High | Low |
| **Setup Complexity** | Simple | Medium | Simple |
| **Test Type** | All | Integration | Unit |
| **Service Coverage** | Supports all via mocking | Many AWS services | All (manual) |
| **Error Testing** | Easy | Easy | Easiest |
| **Real AWS Behavior** | No | High fidelity | Basic responses |
| **Learning Curve** | Easy | Medium | Easy |

---

## Decision Guide

### Use moto if:

✅ **Best for:**
- Testing complex workflows across multiple AWS calls
- Need realistic service behavior (table queries, filters, pagination, etc.)
- Integration testing AWS infrastructure
- Testing business logic that depends on AWS service behavior

**Example scenarios:**
- Testing an ETL pipeline that reads from S3, processes data, writes to DynamoDB
- Testing Lambda functions that query and update DynamoDB
- Testing multi-service workflows (S3 → SNS → Lambda)

```python
def test_etl_pipeline(s3, dynamodb):
    # Use full moto services for realistic integration test
    s3.put_object(Bucket='input-bucket', Key='data.json', Body='...')

    # Your code processes from S3, writes to DynamoDB
    process_pipeline()

    # Verify DynamoDB state
    table = dynamodb.Table('processed_data')
    items = table.scan()
    assert len(items['Items']) > 0
```

### Use botocore.stub if:

✅ **Best for:**
- Unit testing a single function that calls AWS
- Testing specific error scenarios (retries, throttling, timeouts)
- Need fastest possible tests
- Testing precise error handling logic

**Example scenarios:**
- Testing Lambda error handlers
- Testing retry logic with specific AWS errors
- Testing timeout handling
- Testing single function calls

```python
def test_batch_job_status_with_retries(local_batch_stub):
    # Use stub for precise error control
    local_batch_stub.add_client_error('describe_jobs',
                                      service_error_code='ThrottlingException')
    local_batch_stub.add_client_error('describe_jobs',
                                      service_error_code='ServiceUnavailable')
    local_batch_stub.add_response('describe_jobs',
                                 {'jobs': [{'status': 'SUCCEEDED'}]})

    with local_batch_stub:
        # Your retry logic handles specific errors
        response = lambda_handler(event, context)
        assert response['status'] == 'success'
```

### Use pytest alone if:

✅ **Best for:**
- Testing non-AWS code
- Using fixtures for setup/teardown
- Testing business logic without AWS integration

**Example scenarios:**
- Testing utility functions
- Testing data validation
- Testing non-AWS services

```python
def test_addressbook(tmpdir):
    # Pure Python testing without AWS
    addressbook = Addressbook(tmpdir)
    addressbook.add("John", "john@example.com")
    assert addressbook.count() == 1
```

---

## Best Practices from Your Repository

Your repository demonstrates **excellent practices**:

1. **Fixtures in conftest.py**: Centralized AWS service mocking
   ```python
   # Reusable fixtures for all tests
   @pytest.fixture
   def s3():
       with mock_s3():
           yield boto3.client("s3")
   ```

2. **moto for full services**: Integration testing
   ```python
   # Use moto for complete service behavior
   with mock_s3():
       s3 = boto3.client("s3")
   ```

3. **botocore.stub for precise responses**: Unit testing
   ```python
   # Use stub for specific response control
   stubber.add_response("describe_jobs", response)
   ```

4. **Combining tools**: Using both moto and stub together
   ```python
   @pytest.fixture
   def local_batch_stub(mocker, batch, batch_stub):
       # Patch real batch client with stubbed version
       with mocker.patch("module.get_batch", return_value=batch):
           yield batch_stub
   ```

---

## References

- [pytest documentation](https://docs.pytest.org/)
- [moto documentation](https://docs.getmoto.org/)
- [botocore.stub documentation](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/botocore/stub.html)
- [Testing boto3 with pytest fixtures](https://adamj.eu/tech/2019/04/22/testing-boto3-with-pytest-fixtures/)