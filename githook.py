#!/usr/bin/env python
import os, os.path
import json
import subprocess
from ConfigParser import ConfigParser

from flask import Flask, request, redirect, abort
from mock import patch

CONFIG = "config.ini"

app = Flask(__name__)

config = ConfigParser()
config.read(CONFIG)

@app.route('/', methods=['GET'])
def index():
    return redirect('https://github.com/brodul/github-hook')

@app.route('/', methods=['POST'])
def commit():
    payload = request.form.get('payload')
    if not payload:
        return "Missing form variable 'payload'"
    payload = json.loads(payload)
    reponame = payload['repository']['name']
    lastref = payload['ref'].rsplit('/', 1)[1]
    
    if "heads" in payload['ref']:
        branchname = lastref
        cmd = config.get(reponame, branchname)
    elif "tags" in payload['ref']:
        tagname = lastref
        cmd = config.get(reponame + ":tags", tagname)
    else:
        return "Unknown refs!"

    subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)
    return "OK"

application = app # For WSGI

if __name__ == '__main__':
    app.run('localhost')
