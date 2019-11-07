from __future__ import absolute_import, unicode_literals

import os
import pytest
from envbash.read import read_envbash


try:
    FileNotFoundError
except NameError:
    # Python 2
    FileNotFoundError = IOError
    PermissionError = IOError


def test_read_missing_not_ok(tmpdir):
    with pytest.raises(FileNotFoundError):
        read_envbash(str(tmpdir.join('notfound')))


def test_read_missing_ok(tmpdir):
    result = read_envbash(str(tmpdir.join('notfound')), missing_ok=True)
    assert result is None


def test_read_permission_error(tmpdir):
    tmpdir.chmod(0)  # remove all perms
    with pytest.raises(PermissionError):
        read_envbash(str(tmpdir.join('env.bash')))


def test_read_empty(tmpdir):
    orig = dict(os.environ)
    tmpfile = tmpdir.join('env.bash')
    tmpfile.write('')
    result = read_envbash(str(tmpfile))
    assert result == orig


def test_read_normal(tmpdir):
    if 'FOO' in os.environ:
        del os.environ['FOO']
    orig = dict(os.environ)
    tmpfile = tmpdir.join('env.bash')
    tmpfile.write('FOO=BAR')
    result = read_envbash(str(tmpfile))
    assert result['FOO'] == 'BAR'
    del result['FOO']
    assert result == orig


def test_read_error(tmpdir):
    orig = dict(os.environ)
    tmpfile = tmpdir.join('env.bash')
    tmpfile.write('echo ugh >&2\nfalse')
    result = read_envbash(str(tmpfile))
    assert result == orig


def test_read_exit(tmpdir):
    tmpfile = tmpdir.join('env.bash')
    tmpfile.write('exit')
    with pytest.raises(ValueError):
        read_envbash(str(tmpfile))


def test_read_env(tmpdir):
    tmpfile = tmpdir.join('env.bash')
    tmpfile.write('FOO=BAR')
    myenv = {}
    result = read_envbash(str(tmpfile), env=myenv)
    assert result == {'FOO': 'BAR'}


def test_read_fixups(tmpdir):
    tmpfile = tmpdir.join('env.bash')
    tmpfile.write('A=B; C=D; E=F; G=H')
    myenv = {'A': 'Z', 'E': 'F'}
    result = read_envbash(str(tmpfile), env=myenv, fixups=['A', 'C'])
    # there will be extra stuff in result since fixups is overridden, so can't
    # test strict equality.
    assert result['A'] == 'Z'  # fixups, myenv, env.bash
    assert 'C' not in result   # fixups, not myenv, env.bash
    assert result['E'] == 'F'  # not fixups, myenv, env.bash
    assert result['G'] == 'H'  # not fixups, not myenv, env.bash


def test_read_one_arg(tmpdir):
    tmpfile = tmpdir.join('env.bash')
    tmpfile.write('A=$1; B="BAR"')
    myenv = {'A': 'X', 'B': 'Y', 'C': 'BAZ'}
    result = read_envbash(str(tmpfile), env=myenv, args=['FOO'])
    assert result['A'] == 'FOO'
    assert result['B'] == 'BAR'
    assert result['C'] == 'BAZ'


def test_read_three_args(tmpdir):
    tmpfile = tmpdir.join('env.bash')
    tmpfile.write('A=$1; B=$2; C=$3; D="QUX"')
    myenv = {'D': 'Z'}
    result = read_envbash(str(tmpfile), env=myenv, args=['FOO', 'BAR', 'BAZ'])
    assert result['A'] == 'FOO'
    assert result['B'] == 'BAR'
    assert result['C'] == 'BAZ'
    assert result['D'] == 'QUX'


def test_read_space_arg(tmpdir):
    tmpfile = tmpdir.join('env.bash')
    tmpfile.write('A=$1')
    myenv = {'B': 'BAZ'}
    result = read_envbash(str(tmpfile), env=myenv, args=['FOO BAR', 'BAZ'])
    assert result['A'] == 'FOO BAR'
    assert result['B'] == 'BAZ'
