==============
envbash-python
==============

|PyPI| |Build Status| |Coverage Report|

Python module for sourcing a bash script to augment the environment.
Supports Python 2.7 and 3.3+

Rationale
---------

`12-factor apps <https://12factor.net/>`_ require `configuration loaded from the
environment <https://12factor.net/config>`_.

That's `easy on a platform like Heroku
<https://devcenter.heroku.com/articles/config-vars>`_, where the environment is
preset by the user with commands like ``heroku config:set``. But it's messier in
development and non-Heroku deployments, where the environment might need to be
loaded from a file.

This package provides a mechanism for sourcing a Bash script to update Python's
environment (``os.environ``). There are reasons for using a Bash script instead
of another configuration language:

1. Environment variable keys and values should always be strings. Using a Bash
   script to update the environment enforces that restriction, so there won't
   be surprises when you deploy into something like Heroku later on.

2. Using a script means that the values can be sourced into a Bash shell,
   something that's non-trivial if you use a different config language.

3. For better or worse, using a script means that environment variables can be
   set using the full power of the shell, including reading from other files.

Commonly the external file is called ``env.bash``, hence the name of this project.

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

    print(os.environ['FOO'])  #=> prints BAR

Legal
-----

Copyright 2017 `Scampersand LLC <https://scampersand.com>`_

Released under the `MIT license <https://github.com/scampersand/envbash-python/blob/master/LICENSE>`_

.. _PyPI: https://pypi.python.org/pypi/envbash

.. |Build Status| image:: https://img.shields.io/travis/scampersand/envbash-python/master.svg?style=plastic
   :target: https://travis-ci.org/scampersand/envbash-python?branch=master

.. |Coverage Report| image:: https://img.shields.io/codecov/c/github/scampersand/envbash-python/master.svg?style=plastic
   :target: https://codecov.io/gh/scampersand/envbash-python/branch/master

.. |PyPI| image:: https://img.shields.io/pypi/v/envbash.svg?style=plastic
   :target: PyPI_
