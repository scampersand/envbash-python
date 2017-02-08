from __future__ import absolute_import, unicode_literals

import os
import pytest
from envbash.load import load_envbash


def _setup(mocker):
    os.environ['A'] = 'A'
    os.environ['B'] = 'B'
    os.environ['C'] = 'C'
    if 'D' in os.environ:
        del os.environ['D']  # pragma: no cover

    loaded = dict(os.environ, A='a', D='d')
    del loaded['B']

    # mock the call to read_envbash to return our result.
    # frankly this is harder than an env.bash tmpfile but properly unit tests
    # load_envbash.
    read = mocker.patch('envbash.load.read_envbash')
    read.return_value = loaded


def test_load_no_override_no_remove(mocker):
    _setup(mocker)

    # the first argument doesn't matter since read_envbash is mocked
    load_envbash('')

    assert os.environ['A'] == 'A'  # NOT overridden
    assert os.environ['B'] == 'B'  # NOT removed
    assert os.environ['C'] == 'C'  # inherited
    assert os.environ['D'] == 'd'  # loaded


def test_load_override_no_remove(mocker):
    _setup(mocker)

    # the first argument doesn't matter since read_envbash is mocked
    load_envbash('', override=True)

    assert os.environ['A'] == 'a'  # overridden
    assert os.environ['B'] == 'B'  # NOT removed
    assert os.environ['C'] == 'C'  # inherited
    assert os.environ['D'] == 'd'  # loaded


def test_load_no_override_remove(mocker):
    _setup(mocker)

    # the first argument doesn't matter since read_envbash is mocked
    load_envbash('', remove=True)

    assert os.environ['A'] == 'A'  # NOT overridden
    assert 'B' not in os.environ   # removed
    assert os.environ['C'] == 'C'  # inherited
    assert os.environ['D'] == 'd'  # loaded


def test_load_override_remove(mocker):
    _setup(mocker)

    # the first argument doesn't matter since read_envbash is mocked
    load_envbash('', override=True, remove=True)

    assert os.environ['A'] == 'a'  # overridden
    assert 'B' not in os.environ   # removed
    assert os.environ['C'] == 'C'  # inherited
    assert os.environ['D'] == 'd'  # loaded


def test_load_into(mocker):
    read = mocker.patch('envbash.load.read_envbash')
    read.return_value = {'A': 'B'}
    orig = dict(os.environ)
    into = {}
    load_envbash('', into=into)
    assert into == {'A': 'B'}
    assert dict(os.environ) == orig


