python-pytest
---------------------------------------------------------------
Python unit testing using - pytest, moto - mock_s3,mock_dynamodb etc, botocore.stub, pytest-spark - pyspark, sparksql. 
When using pytest the test case will indicate that it needs some kind of resource or test fixture
by specifying arguments to the test function. Pytest will then go and look for a function decorated
with this **pytest.fixture decorator**, and it should have the same name as the resource the test is
requesting, and then at runtime, it will hook it altogether. It's a kind of dependency injection. The test 
just declares, I'm going to need a resource, but it doesn't need to know where it comes from; it will just
rely on being given one before it's time to execute.

Lets write test fixture addressbook, [see](tests/conftest.py), we decorate this new addressbook function with the pytest.fixture decorator, the pytest connects addressbook function and test method with addressbook argument together  at runtime. We define this test fixture addressbook and pass it as an argument in the [test method](tests/test_addressbook.py) and it will return Addressbook, instead of constructing it directly - by this I mean  Addressbook(tmpdir). This fixture mechanism does rely on you not making a typo when you write the name of the resource. If there is a typo Pytest will give a clear error message that it can't find the fixture for the resource addressbook. It will list all the fixtures that are available, there are
quite a lot of fixtures on the list even though we've only defined one addresbook typo. See [src](/src) 
and [tests](/tests)

# Notes
- pytest --fixtures, lists all the available fixtures, default ones and the one that are in your package.
  In one of our examples we use default fixture **tmpdir**
  <pre>
  tmpdir
    Return a temporary directory path object which is unique to each test
    function invocation, created as a sub directory of the base temporary
    directory.

    By default, a new base temporary directory is created each test session,
    and old bases are removed after 3 sessions, to aid in debugging. If
    ``--basetemp`` is used then it is cleared each session. See :ref:`base
    temporary directory`.
  </pre>
- pytest --markers, lists all the markers
- pytest-html plugin, gives you html pytest report

## Setup code
- virtualenv venv
- venv\Scripts\activate
- pip install -r requirements.txt  
- setup.py install
- pytest --fixtures src
### run tests
- setup.py develop
- pytest tests or pytest 


## magic of conftest.py
conftest.py, contains our test fixtures for example, addressbook is a test fixture. This module has a special
meaning for pytest. By defining conftest.py in your root path, you will have pytest recognizing your 
application modules without specifying PYTHONPATH. Any fixtures you put here in conftest will be available
to all the test modules in this folder and subfolders, in our case everything under folder tests. Another 
important file for pytest is this ini file kept in the root folder of the project. This contains project-wide
pytest configuration and we can change the behavior of the pytest test runner.
 
The fixtures that you will define in conftest.py will be shared among all tests in your test suite. However,
defining fixtures in the root conftest.py might slow down testing if such fixtures are not used by all tests.
[see](https://stackoverflow.com/questions/34466027/in-pytest-what-is-the-use-of-conftest-py-files)

## Use case 1, moto
- In this test case we use pytest, moto - mock_s3,mock_dynamodb 
SNS triggers the lambda, this [sns event](src/aws/lambda_events_data/sns_lambda.json) is parsed by the aws lambda handler.
This message has s3 location shared by the producer. The s3 object metadata has the record count. The lambda updates the dynamodb with the s3 object location
,the record count and more into  dynamodb.

The [working copy](src/aws/README.md) of the source code using serverless framework, which create sns topic 'dispatch*', creates a 
lambda and associates the sns topic with the aws lambda. This lambda is triggered by SNS. You need to attach this 
policy file to your aws cli user account

conftest.py has all the fixtures defined which are used by this use case.
In our py tests we check out the following in our code:
- s3 object read
- s3 record count
- s3 metadata read the recored count set by producers
- dynamodb update

## Use Case 2, botocore.stub
- here will be using pytest, botocore.stub
lambda to check the batch job status, with 3 retry attempts with 10 second backoff interval. In the first two attempts
boto3 batch job describe api throw exceptions and finally it succeeds in the last and the final attempt. For this use case
we will be using botocore.stub.Stubber.  Note in the case of stubber the boto3 batch client handle is shared b/w the 
tested module and the testing module. Also the fixture is not defined in conftest.py as this is one off and written directly
with the [test module](tests/test_check_batchjob_status.py). In this use case i think botocore.stub is the only option and 
this is only option I know as of now how to implement.
- [Stubber, see client error](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html)

### Cons with using botocore stub
- They require a lot more prep. Creating stubs is time-consuming. 
- They’re fragile and fake. Responses are returned first in, first out - so if you call the  APIs in a different order
  than you added the responses, it will throw an error. 
- To make the stubs look somewhat realistic, you have to mock many fields that your code doesn’t care about and bloat 
  your tests with fake responses.
- They leak implementation details from the module being tested. For example, if a module switched from using s3.list_objects to s3.list_objects_v2, 
  the test would fail because it depends on a specific API being called. This creates an unnecessary dependency on t
  he private API of the module, instead of testing the public API.


## localstack
Another option is localstack, which allows you to bring up an entire AWS cloud stack locally. To add 

## Use Case - pyspark, pytest-spark
When it comes to unit testing PySpark pipeline code, one good way is to encapsulate the critical ETL transforms of a 
pySpark script inside a method/function, [see example](./src/bigdata/etl_transform.py). Install 
packages - pytest-spark, pyspark. Also [setup local spark](https://github.com/paramraghavan/sparksql-awsglue/blob/main/help/sparksql-setup.md)
- pip install pyspark 
- pip install pytest-spark
- Add “spark_home” value to pytest.ini in your project directory:
<pre>
For Mac/Unix
[pytest]
spark_home = /opt/spark
 
For Windows
[pytest]
spark_home = C:\Users\padma\spark\spark-sql\tools\spark-3.1.2-bin-hadoop2.7
</pre>


References
---------------
- https://pypi.org/project/pytest-spark/
- https://www.confessionsofadataguy.com/introduction-to-unit-testing-with-pyspark/


### Notes
<pre>
  install virtualenv
  Virtual env --> https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
  py -m pip install virtualenv / python -m pip install virtualenv
  create virtual env and activate
  virtualenv venv
  venv\Scripts\activate
</pre>
- [3 ways to test S3 in Python](https://www.sanjaysiddhanti.com/2020/04/08/s3testing/)
