=======
githook
=======

Simple Flask application that runs a script in response of GitHub post hook.

.. image:: https://secure.travis-ci.org/brodul/githook.png?branch=master

Inspired by:

https://github.com/hasgeek/github-hook

How to use
==========

* Git clone

* cd githook

* Create a config.ini (please refer to the example.ini)

*
    python bootstrap.py -d

*
    bin/buildout

*
    bin/supervisord

githook now listens on port 5000 port for for post request from github

you still need to configure nginx or apache to make a proxy pass
look at the nginx.conf

Tests
=====

To run tests use:

bin/python tests/test.py

TODO
====

See github issues.
