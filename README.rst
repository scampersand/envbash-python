==============
envbash-python
==============

|PyPI| |Build Status| |Coverage Report| |Python Versions|

Python module for sourcing a bash script to augment the environment.
Supports Python 2.7 and 3.4+

Rationale
---------

`12-factor apps <https://12factor.net/>`__ require `configuration loaded
from the environment <https://12factor.net/config>`__.

That's `easy on a platform like
Heroku <https://devcenter.heroku.com/articles/config-vars>`__, where the
environment is preset by the user with commands like
``heroku config:set``. But it's messier in development and non-Heroku
deployments, where the environment might need to be loaded from a file.

This package provides a mechanism for sourcing a Bash script to update
Python's environment (``os.environ``). Commonly the external file is called
``env.bash``, hence the name of this project.

Installation
------------

Install from PyPI_:

.. code:: sh

    pip install envbash

Usage
-----

Call ``load_envbash`` to source a Bash script into the current Python process.
Any variables that are set in the script, regardless of whether they are
explicitly exported, will be added to the process environment.

For example, given ``env.bash`` with the following content:

.. code:: sh

    FOO='bar baz qux'

This can be loaded into Python:

.. code:: python

    import os
    from envbash import load_envbash

    load_envbash('env.bash')

    print(os.environ['FOO'])  #=> bar baz qux

FAQ
---

How is this different from `dotenv <https://github.com/theskumar/python-dotenv>`__?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both projects aim to solve the same problem, but differ in approach. In
particular, dotenv uses an ad hoc config syntax whereas envbash uses
Bash.

dotenv's syntax becomes a problem with multi-line strings. dotenv intends for
the ``.env`` file to be readable by the shell, but the dotenv format for
multi-line strings isn't compatible with the shell.

If the point is to have a configuration language that's well-suited to
environment variables, it's hard to beat pure Bash, and it's guaranteed
to source properly into the shell.

Should I commit ``env.bash`` to source control?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No, definitely not. The purpose of ``env.bash`` is to store development
configuration that isn't suitable for committing to the repository,
whether that's secret keys or developer-specific customizations. In
fact, you should add the following line to ``.gitignore``:

::

    /env.bash

Is it necessary to explicitly ``export`` variables in ``env.bash``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No, envbash prefixes sourcing your ``env.bash`` with ``set -a`` which
causes all newly-set variables to be exported automatically. If you
would rather explicitly export variables, you can ``set +a`` at the top
of your ``env.bash``.

How do I put a multi-line string into ``env.bash``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can put newlines directly into a multi-line string in Bash, so for
example this works:

.. code:: bash

    PRIVATE_KEY="
    -----BEGIN RSA PRIVATE KEY-----
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    -----END RSA PRIVATE KEY-----"

Does envbash override my environment settings?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default your local environment settings win, so you can override the
content of ``env.bash`` by explicitly exporting variables in your shell.

You can change this behavior. This makes sense for a deployed instance
that gets full configuration from ``env.bash`` and needs to be protected
from the calling environment.

.. code:: python

    load_envbash('env.bash', override=True)

Can I remove settings from the environment?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default envbash doesn't remove settings, but you can change this
behavior.

.. code:: python

    load_envbash('env.bash', remove=True)

This will cause any variables that you explicitly ``unset`` in
``env.bash`` to be removed from Python's ``os.environ`` as well.

How do I source ``env.bash`` into my guest shell environment?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming that your source directory is available on the default
``/vagrant`` mount point in the guest, you can add add this line at the
bottom of ``/home/vagrant/.bash_profile``:

::

    set -a; source /vagrant/env.bash; set +a

Note that this means that settings are loaded on ``vagrant ssh`` so you
need to exit the shell and rerun ``vagrant ssh`` to refresh if you
change settings.

What about Ruby?
~~~~~~~~~~~~~~~~~~

See `envbash-ruby <https://github.com/scampersand/envbash-ruby>`__

Legal
-----

Copyright 2017-2018 `Scampersand LLC <https://scampersand.com>`_

Released under the `MIT license <https://github.com/scampersand/envbash-python/blob/master/LICENSE>`_

.. _PyPI: https://pypi.python.org/pypi/envbash

.. |Build Status| image:: https://img.shields.io/travis/scampersand/envbash-python/master.svg?style=plastic
   :target: https://travis-ci.org/scampersand/envbash-python?branch=master

.. |Coverage Report| image:: https://img.shields.io/codecov/c/github/scampersand/envbash-python/master.svg?style=plastic
   :target: https://codecov.io/gh/scampersand/envbash-python/branch/master

.. |PyPI| image:: https://img.shields.io/pypi/v/envbash.svg?style=plastic
   :target: PyPI_

.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/envbash.svg?style=plastic
   :target: PyPI_
