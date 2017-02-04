from __future__ import absolute_import, unicode_literals

from functools import partial
import os
import envbash


def test_module_exports():
    """
    Test that the envbash package exports the expected symbols.
    """
    exports = [k for k in dir(envbash) if not k.startswith('_')]
    need = ['load_envbash', 'read_envbash']
    assert all(n in exports for n in need)


def test_through(tmpdir):
    """
    integration test load/read to os.environ
    """
    tmpfile = tmpdir.join('env.bash')
    tmpfile.write('FOO=BAR')
    if 'FOO' in os.environ:
        del os.environ['FOO']
    envbash.load_envbash(str(tmpfile))
    assert os.environ['FOO'] == 'BAR'
