"""Shared fixtures."""

import pytest

from addressbook import Addressbook


@pytest.fixture
def addressbook(tmpdir):
    """Provides an empty Addressbook"""
    return Addressbook(tmpdir)

