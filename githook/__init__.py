#!/usr/bin/env python
from ConfigParser import ConfigParser
from optparse import OptionParser
import json
import logging
import subprocess
import sys

from flask import Flask, request, redirect


class ConfigNotFoundError(Exception):
    """docstring for ConfigNotFound"""
    pass

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

def test_config(config):
    """This function tests the ConfigParser object if the INI is as we want it.
    Writes errors to log.

    Returns list of errors (str) for testing.
    """
    msg_list = []
    for section in config.sections():
        for option in ["name", "owner", "cmd"]:
            if not config.has_option(section, option):
                msg = 'Section "%s" must have "%s" option!' % (section, option)
                msg_list.append(msg)
                logging.critical(msg)
            hastag = config.has_option(section, "tag")
            hasbranch = config.has_option(section, "branch")
        if hastag and hasbranch:
            msg = 'Please put only tag OR branch option in the "%s" section!' % section
        elif not (hastag or hasbranch):
            msg = 'Please put tag OR branch option in the "%s" section!' % section
        else:
            continue
        msg_list.append(msg)
        logging.critical(msg)
    return msg_list


@app.route('/', methods=['GET'])
def index():
    """Simple function called if we get a GET request.
    Redirects to githook repo on github.
    """
    return redirect('https://github.com/brodul/githook')


@app.route('/', methods=['POST'])
def commit():
    """ #TODO"""

    config = app.config["iniconfig"]

    payload = request.form.get('payload')
    if not payload:
        return "Missing form variable 'payload'"
    payload = json.loads(payload)

    ref = payload["ref"]
    refend = ref.rsplit("/", 1)[1]

    owner = payload["repository"]["owner"]["name"]
    reponame = payload["repository"]["name"]

    run = lambda cmd: subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)

    mached = False
    for section in config.sections():
        config_tag, config_branch = None, None
        config_owner = config.get(section, "owner")
        config_name = config.get(section, "name")
        if not (config_owner == owner and config_name == reponame):
            continue
        cmd = config.get(section, "cmd")
        if config.has_option(section, "tag"):
            config_tag = config.get(section, "tag")
        elif config.has_option(section, "branch"):
            config_branch = config.get(section, "branch")
        if refend in (config_branch, config_tag):
            run(cmd)
            logging.info("Section: %s mached." % section)
            mached = True

    if not mached:
        msg = "No section mached!"
        logging.warning(msg)
        return msg

    return "OK"


def cli_run():
    """Entry point funcion for CLI."""
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="configfile", default="./config.ini",
                      help="INI file config [default: %default]", metavar="FILE")
    parser.add_option("-l", "--listen",
                      dest="address", default="localhost",
                      help="hostname to listen on [default: %default]")
    parser.add_option("-p", "--port",
                      dest="port", default="5000",
                      help="the port of githook [default: %default]")

    (opt, args) = parser.parse_args()

    config = ConfigParser()
    if not config.read(opt.configfile):
        raise ConfigNotFoundError

    error = test_config(config)

    if error:
        sys.exit(1)

    # pass configparser object to Flask
    app.config["iniconfig"] = config

    app.run(opt.address, int(opt.port))

if __name__ == '__main__':
    cli_run()
