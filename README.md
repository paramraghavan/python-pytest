# python-pytest
python aws unit testing  - pytest, mock, moto, botocore.stub. We will be focussing on pytest
When using Pytest the test case will indicate that it needs some kind of resource or test fixture
by specifying arguments to the test function. Pytest will then go and look for a function decorated
with this **pytest.fixture decorator**, and it should have the same name as the resource the test is
requesting, and then at runtime, it will hook it altogether. It's a kind of dependency injection. The test 
just declares, I'm going to need a resource, but it doesn't need to know where it comes from; it will just
rely on being given one before it's time to execute.

## Use case 1
sns triggers lambda. Sns messgae which is read in  lambda has the s3 location with lambda and lambda saves the s3 location into dynamo db table

## Use Case 2
lambda to check the batch job status, with 3 retry attempt with 10 second backoff interval.


## Use Case 3
It's like use case 1, except that the S3 needs a cross account bucket access and s3 metadata has cehcksum value which needs to read and stored into dynamo db




