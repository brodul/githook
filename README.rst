=======
githook
=======

Simple Flask application that runs a script in response of GitHub post hook.

.. image:: https://secure.travis-ci.org/brodul/githook.png?branch=master

Inspired by:

https://github.com/hasgeek/github-hook

How to install and use
======================

* Git clone

* ``cd githook``

* Create a config.ini (please refer to the example.ini)

* run the following commands:

    *
        ``python bootstrap.py -d``

    *
        ``bin/buildout``

    *
        ``bin/supervisord``

OR

* Install the githook package via ``pip``, ``easy_install`` or ``buildout``

* githook (script) will appear in you bin PATH

* just run ``githook``

githook now listens on port 5000 port for for post request from github

example.ini
===========

.. literal:: example.ini

Githook command line usage
==========================

You can access the help always with the ``-h`` or ``--help`` option
::
    
    Usage: githook [options]

    Options:
      -h, --help            show this help message and exit
      -c FILE, --config=FILE
                            INI file config [default: ./config.ini]
      -l ADDRESS, --listen=ADDRESS
                            hostname to listen on [default: localhost]
      -p PORT, --port=PORT  the port of githook [default: 5000]

Nginx configuration
===================

you still need to configure nginx or apache to make a proxy pass

.. literal:: nginx.conf

Apache configuration
====================

TODO

Tests
=====

To run tests use:

``bin/test``

TODO
====

See github issues.

:mushroom:
