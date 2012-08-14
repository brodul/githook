#!/usr/bin/env python
import os, os.path
import json
import subprocess
from ConfigParser import ConfigParser
from ConfigParser import NoSectionError
from ConfigParser import NoOptionError

from flask import Flask, request, redirect, abort

CONFIG = "config.ini"

app = Flask(__name__)

config = ConfigParser()
config.read(CONFIG)

@app.route('/', methods=['GET'])
def index():
    return redirect('https://github.com/brodul/githook')

@app.route('/', methods=['POST'])
def commit():
    payload = request.form.get('payload')
    if not payload:
        return "Missing form variable 'payload'"
    payload = json.loads(payload)
    reponame = payload['repository']['name']
    lastref = payload['ref'].rsplit('/', 1)[1]
    
    try:
        if "heads" in payload['ref']:
            branchname = lastref
            cmd = config.get(reponame, branchname)
        elif "tags" in payload['ref']:
            tagname = lastref
            section = reponame + ":tags"
            cmd = config.get(section, tagname)
    except NoSectionError:
        return "Unknown section!"
    except NoOptionError:
        return "Unknown branch or tag!"

    subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)
    return "OK"

application = app # For WSGI

if __name__ == '__main__':
    app.run('localhost')
