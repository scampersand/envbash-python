from __future__ import absolute_import, unicode_literals

import os
import pytest
from envbash.load import load_envbash


def test_load_add_remove(mocker):
    # original environ lacks A but has C and E
    if 'A' in os.environ:
        del os.environ['A']
    os.environ['C'] = 'D'
    os.environ['E'] = 'F'

    # loaded environ overrides A, inherits C and removes E
    loaded = dict(os.environ, A='B')
    del loaded['E']

    # mock the call to read_envbash to return our result.
    # frankly this is harder than an env.bash tmpfile but properly unit tests
    # load_envbash.
    read = mocker.patch('envbash.load.read_envbash')
    read.return_value = loaded

    # the first argument doesn't matter since read_envbash is mocked
    load_envbash('')

    assert os.environ['A'] == 'B'  # loaded
    assert os.environ['C'] == 'D'  # inherited
    assert 'E' not in os.environ   # removed


def test_load_no_remove(mocker):
    read = mocker.patch('envbash.load.read_envbash')
    read.return_value = {}  # would remove everything
    orig = dict(os.environ)
    load_envbash('', remove=False)
    assert dict(os.environ) == orig


def test_load_into(mocker):
    read = mocker.patch('envbash.load.read_envbash')
    read.return_value = {'A': 'B'}
    orig = dict(os.environ)
    into = {}
    load_envbash('', into=into)
    assert into == {'A': 'B'}
    assert dict(os.environ) == orig


