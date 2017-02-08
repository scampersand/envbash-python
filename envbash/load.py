from __future__ import absolute_import, unicode_literals

import os
from .read import read_envbash


def load_envbash(envbash, into=os.environ, override=False, remove=False, **kwargs):
    """
    Load ``envbash`` into ``into`` (default ``os.environ``).
    """
    loaded = read_envbash(envbash, **kwargs)
    if loaded is not None:
        if remove:
            for k in set(into) - set(loaded):
                del into[k]
        if override:
            into.update(loaded)
        else:
            for k in set(loaded) - set(into):
                into[k] = loaded[k]
