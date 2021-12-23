import pytest

from addressbook import Addressbook

'''
We have not defined the fixture here on purpose and not inside conftest.py
So this can be an simple independent example.
Commented out here as it is used from conftest.py
'''
# @pytest.fixture
# def addressbook(tmpdir):
#     "Provides an empty Phonebook"
#     return Addressbook(tmpdir)


def test_lookup_by_name(addressbook):
    addressbook.add("Duncan", "1234 Cape Cod MA")
    assert "1234 Cape Cod MA" == addressbook.lookup("Duncan")


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