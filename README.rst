=======
githook
=======

Simple Flask application that runs a script in response of GitHub post hook.


Inspired by:

https://github.com/hasgeek/github-hook

How to use
==========

* Git clone

* Create a config.ini (please refer to the config.example.ini)

*
    python bootstrap.py -d

*
    bin/buildout

*
    bin/python githook.py

githook now listens on port 5000 port for for post request from github

you still need to configure nginx or apache to make a proxy pass

TODO
====

See github issues.
