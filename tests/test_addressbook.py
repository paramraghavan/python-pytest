import pytest

from addressbook import Addressbook

'''
We have not defined the fixture here on purpose and not inside conftest.py
So this can be an simple independent example.
Commented out here as it is used from conftest.py
'''
# @pytest.fixture
# def addressbook(tmpdir):
#     "Provides an empty Addressbook"
#     return Addressbook(tmpdir)

'''
Resource address book injected
'''
def test_lookup_by_name(addressbook):
    addressbook.add("Duncan", "1234 Cape Cod MA")
    assert "1234 Cape Cod MA" == addressbook.lookup("Duncan")


'''
This will be skipped because of WIP - work in progress tag 
'''
@pytest.mark.skip("WIP")
def test_phonebook_contains_all_names_skip(addressbook):
    addressbook.add("Duncan", "1234 Cape Cod MA")
    assert "Duncan" in addressbook.names()

def test_phonebook_contains_all_names(addressbook):
    addressbook.add("Duncan", "1234 Cape Cod MA")
    assert "Duncan" in addressbook.names()

'''
If you notice the addressbook has  been initialized 
but user 'Duncan' has not been added to the addressbook.
So in this use case we expect an exception to be raised
and the test will be successful
'''
def test_missing_name_raises_error(addressbook):
    with pytest.raises(KeyError):
        addressbook.lookup("Duncan")

'''
Imagine in this test you reading a 100 mb file and doing some sort of
processing and you may want to skip this test when you are doing development
so you tests run are quick.

We have marked this test as slow. That means that we can add a directive to the pytest runner,
that it should exclude tests with this mark. Executing pytest with additional argument  
"pytest runner -m not slow", and this test case will be excluded.

This marker "slow" is defined in pytest.ini
'''
@pytest.mark.slow
def test_large_file(addressbook):
    pass