=======
githook
=======

.. note::  This project is discontinued. If you are seaching for a similar project, please look at https://github.com/bbinet/hooked .

This application starts a small web server, 
reads a INI config file and listens for GitHub post requests,
then runs a script in response of the post request.


.. image:: https://secure.travis-ci.org/brodul/githook.png?branch=master

Inspired by:

https://github.com/hasgeek/github-hook

How to install (for sysadmins)
==============================

* Install ``python-setuptools`` for your distribution (It is possible you already have it installed.)

* Install the githook package ``sudo easy_install githook``

* Create a configuration file.  

* just run ``githook -c $PATH_TO_YOUR_CONFIG``

.. note::
    
    For configuration file example see below.

.. note::

    Githook will not daemonize itself. 
    It's recommended to use it with supervisord project
    or write an init script. 
    If you would like to have this feature write a comment on github.

How to install from GitHub
==========================

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


githook now listens on port 5000 port for for post request from github

example.ini
===========

Example
::

    [something]
    ; This section will match if you push commit or more commits to project/repo "test" branch "master"

    ; You must specify the project/repository name
    name=test

    ; You must specify your username or the name of the organization
    owner=brodul

    ; You must specify branch
    branch=master

    ; The command that will be executed on match
    cmd=ls

    ; comment
    # comment

    [willmatch]
    ; All the sections that match will be executed
    name=test
    owner=brodul
    branch=master
    cmd=pwd


    [tagmatch]
    name=test
    owner=brodul
    ; This will match on tag move, delete, create ...
    tag=trololo
    cmd=pwd


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

Example
::

    server {
            listen   80 ;
            server_name domain.com;

            access_log  /var/log/nginx/githook.access.log;
            error_log  /var/log/nginx/githook.error.log;


            location /githook {

                    # Allow github IPs
                    allow 207.97.227.253; 
                    allow 50.57.128.197;
                    allow 108.171.174.178;
                    deny all;

                    rewrite /githook / break;

                    proxy_pass http://localhost:5000 ;

            }

Apache configuration
====================

TODO

Tests
=====

To run tests use:

``bin/nosetests``

TODO
====

See github issues.
