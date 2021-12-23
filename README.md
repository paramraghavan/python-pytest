python-pytest
---------------------------------------------------------------

python aws unit testing  - pytest, mock, moto, botocore.stub. We will be focussing on pytest
When using Pytest the test case will indicate that it needs some kind of resource or test fixture
by specifying arguments to the test function. Pytest will then go and look for a function decorated
with this **pytest.fixture decorator**, and it should have the same name as the resource the test is
requesting, and then at runtime, it will hook it altogether. It's a kind of dependency injection. The test 
just declares, I'm going to need a resource, but it doesn't need to know where it comes from; it will just
rely on being given one before it's time to execute.

Let's write a test fixture in this example code. I'm going to extract a method that will return the 
addressbook, and then I can add it as an argument in the test method instead of constructing it directly.
If we decorate the new function with the pytest.fixture decorator, then pytest will connect them together 
at runtime. We can use the same fixture in the other two test cases as well. Now when I run all the
test cases, they all still passed. This fixture mechanism does rely on you not making a typo when you 
write the name of the resource. If there is a type Pytest will give a clear error message that it can't
find the fixture for the resource addressbook. It will list all the fixtures that are available, there are
quite a lot of fixtures on the list even though we've only defined one addresbook typo. See [src](\src) 
and [tests](\tests)

# Notes
- pytest --fixtures, lists all the available fixtures, default ones and the one that are in your package
- pytest --markers, lists all the markers
- pytest-html plugin, gives you html pytest report

## Setup code
python setup.py install

## magic of conftest.py
conftest.py, contains our test fixtures for example addressbook is a test fixture. This module has a special
meaning for pytest. By defining conftest.py in your root path, you will have pytest recognizing your 
application modules without specifying PYTHONPATH. Any fixtures you put here in conftest will be available
to all the test modules in this folder and subfolders, in our case everything under folder tests. Another 
important file for pytest is this ini file kept in the root folder of the project. This contains project-wide
pytest configuration and we can change the behavior of the pytest test runner.
 
The fixtures that you will define in conftest.py will be shared among all tests in your test suite. However,
defining fixtures in the root conftest.py might slow down testing if such fixtures are not used by all tests.
[see](https://stackoverflow.com/questions/34466027/in-pytest-what-is-the-use-of-conftest-py-files)

## Use case 1
sns triggers lambda. Sns messgae which is read in  lambda has the s3 location with lambda and lambda saves the s3 location into dynamo db table

## Use Case 2
lambda to check the batch job status, with 3 retry attempt with 10 second backoff interval.


## Use Case 3
It's like use case 1, except that the S3 needs a cross account bucket access and s3 metadata has cehcksum value which needs to read and stored into dynamo db




