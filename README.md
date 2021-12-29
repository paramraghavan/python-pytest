python-pytest
---------------------------------------------------------------
Python unit testing using - pytest, mock, moto, botocore.stub. 
When using pytest the test case will indicate that it needs some kind of resource or test fixture
by specifying arguments to the test function. Pytest will then go and look for a function decorated
with this **pytest.fixture decorator**, and it should have the same name as the resource the test is
requesting, and then at runtime, it will hook it altogether. It's a kind of dependency injection. The test 
just declares, I'm going to need a resource, but it doesn't need to know where it comes from; it will just
rely on being given one before it's time to execute.

Lets write test fixture addressbook, [see](tests/conftest.py). We are going to extract a method that will return the 
Addressbook, and then we  add it as an argument in the [test method](tests/test_addressbook.py) instead of constructing it directly.
If we decorate this new addressbook function with the pytest.fixture decorator, then pytest will connect them together 
at runtime. We can use the same fixture in the other test cases as well. This fixture mechanism does rely on you not making a typo when you 
write the name of the resource. If there is a typo Pytest will give a clear error message that it can't
find the fixture for the resource addressbook. It will list all the fixtures that are available, there are
quite a lot of fixtures on the list even though we've only defined one addresbook typo. See [src](/src) 
and [tests](/tests)

# Notes
- pytest --fixtures, lists all the available fixtures, default ones and the one that are in your package
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

## Use case 1
SNS triggers the lambda, this event is parsed by the aws lambda handler.
The message has s3 location shared by the producer. The s3 object metadata has the record count,
[sns event](src/aws/lambda_events_data/sns_lambda.json). The lambda updates the dynamodb with the s3 object location
,the record count and more into  dynamodb.

The [working copy](src/aws/README.md) of the source code using serverless framework, which create sns topic 'dispatch*', creates a 
lambda and associates the sns topic with the aws lambda. This lambda is triggered by SNS. You need to attach this 
policy file to your aws cli user account

conftest.py has all the fixtures defined which are used by this use case.
In our py tests we check out the following in our code:
- s3 file read
- s3 record count
- s3 metadata read the recored count set by producers
- dynamodb update

## Use Case 2
lambda to check the batch job status, with 3 retry attempt with 10 second backoff interval.


## Use Case 3
It's like use case 1, except that the S3 needs a cross account bucket access and s3 metadata has cehcksum value which needs to read and stored into dynamo db


### Notes
<pre>
  install virtualenv
  Virtual env --> https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
  py -m pip install virtualenv / python -m pip install virtualenv
  create virtual env and activate
  virtualenv venv
  venv\Scripts\activate
</pre>

