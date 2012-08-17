#!/usr/bin/env python
import json
import subprocess
from optparse import OptionParser
from ConfigParser import ConfigParser
from ConfigParser import NoSectionError
from ConfigParser import NoOptionError

from flask import Flask, request, redirect


class ConfigNotFoundError(Exception):
    """docstring for ConfigNotFound"""
    pass

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return redirect('https://github.com/brodul/githook')


@app.route('/', methods=['POST'])
def commit():

    config = app.config["iniconfig"]

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


def cli_run():
    """docstring for fname"""
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="configfile", default="config.ini",
                      help="INI file config", metavar="FILE")
    parser.add_option("-l", "--listen",
                      dest="address", default="localhost",
                      help="hostname to listen on")
    parser.add_option("-p", "--port",
                      dest="port", default="5000",
                      help="the port of githook")

    (opt, args) = parser.parse_args()

    config = ConfigParser()
    if not config.read(opt.configfile):
        raise ConfigNotFoundError

    # pass configparser object to Flask
    app.config["iniconfig"] = config

    app.run(opt.address, int(opt.port))

if __name__ == '__main__':
    cli_run()
