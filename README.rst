======
Lancet
======

|pypi| |build| |coverage|

From http://en.wikipedia.org/wiki/Scalpel:

    A scalpel, or lancet, is a small and extremely sharp bladed instrument used
    for surgery, anatomical dissection, and various arts and crafts (called a
    hobby knife).

Lancet is a command line utility to streamline the various activities related
to the development and maintenance of a software package.


Contributing
============

This is a an open-source project. We'll be delighted to receive your
feedback in the form of issues and pull requests.

We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/divio/lancet/graphs/contributors>`_
section.


Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/divio/lancet/blob/master/setup.py>`_
file for additional dependencies:

|python|

Please refer to the documentation in the docs/ directory for more information or visit our
`online documentation <http://lancet.readthedocs.org/en/latest/installation/>`_.


Getting started
---------------

Once `installed <http://lancet.readthedocs.org/en/latest/installation/>`_,
set up the initial configuration by running::

   lancet setup

For each not-yet-configured project, you can then run::

   cd path/to/project
   lancet init

This creates a new project-level configuration file that can be shared across
different users (and thus commited to source control).


Running Tests
-------------

You can run tests by executing::

    virtualenv env
    source env/bin/activate
    pip install -r lancet/test/requirements.txt
    python setup.py test


.. |pypi| image:: https://badge.fury.io/py/lancet.svg
    :target: http://badge.fury.io/py/lancet
.. |build| image:: https://travis-ci.org/divio/lancet.svg?branch=master
    :target: https://travis-ci.org/divio/lancet
.. |coverage| image:: https://codecov.io/gh/divio/lancet/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/divio/lancet

.. |python| image:: https://img.shields.io/badge/python-3.4%20%7C%203.5%20%7C%203.6%20%7C%203.7-blue.svg
    :target: https://pypi.org/project/lancet/
