import logging
import signal
import time
from dotenv import load_dotenv
from os import environ, path
import os
from flask import request, jsonify, render_template, url_for#,redirect
import subprocess
from subprocess import check_output
import flask
import argparse
import sys
from DLFlib.DebianAPILib import *
from DLFlib.DBFeedLib import *
'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''
# Load .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
# Load parametrs from .env file
PATH = environ.get('PATH')
LOGFILE = environ.get('LOGFILE')
PORT = environ.get('PORT')
HOST = environ.get('HOST')
GITREPO = environ.get('GITREPO')
SHUTDOWN = environ.get('SHUTDOWN')
# API Shutdown function
PID = os.getpid()




def shutdown(secs):
    print("Shutting down server in:")
    for i in range(int(secs), 0, -1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)
    os.kill(int(PID), signal.SIGINT)


# Check the port number range
class PortAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not 0 < values < 2**16:
            raise argparse.ArgumentError(
                self, "port numbers must be between 0 and 65535")
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port",
                    help='Port number to connect to',
                    dest='port',
                    # default=PORT,
                    type=int,
                    action=PortAction,
                    metavar="{0..65535}")
parser.add_argument("-P", "--PATH",
                    help='PATH environment override',
                    dest='PATH',
                    # default=environ.get('PYTHONHOME'),
                    type=str)
parser.add_argument("-s", "--shutdown",
                    help='shutdown timer express in seconds',
                    dest='shutdown',
                    # default="SHUTDOWN",
                    type=str)
args = parser.parse_args()
if args.port:
    PORT = args.port
if args.PATH:
    PATH = args.PATH
if args.shutdown:
    SHUTDOWN = args.shutdown
os.environ['PATH'] = PATH



app = flask.Flask(__name__)
app.config["DEBUG"] = True
# logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)


@app.route('/APIEndpoints')
def APIEndpoints():
    return render_template('APIEndpoints.html')

@app.route('/populateDB', methods=['POST', 'GET'])
def populateDBEndpoint():
    args = request.args
    packageNameAndVersion = args['packageNameAndVersion']
    packageNameAndVersion = packageNameAndVersion.split(",")
    packageName = packageNameAndVersion[0]
    packageVersion = packageNameAndVersion[1]
    print(packageName)
    print(packageVersion)
    # first populate the DB with a package
    package_version_id = PopulateDB(packageName,packageVersion)
    print(package_version_id)
    return str(package_version_id)




@app.route('/DebianPackageVersion', methods=['POST', 'GET'])
def GetDebianPackageVersion():
    args = request.args
    packageNameAndVersion = args['packageNameAndVersion']
    packageNameAndVersion = packageNameAndVersion.split(",")
    packageName = packageNameAndVersion[0]
    packageVersion = packageNameAndVersion[1]
    print(packageName)
    print(packageVersion)
    DebianChecksumCollector(packageName,packageVersion)
    DebianLicenseCollector(packageName,packageVersion)
    FeedLicenseForFile(packageName,packageVersion)

    output = "Elaborating "+packageName+", version "+packageVersion+" ... "
    return output



@app.route('/shutdown/', defaults={"secs": "1"})
@app.route('/shutdown/<secs>')
def shutd(secs):
    shutdown(int(secs))
    return "Shutting down server"


@app.route('/PATH', methods=['GET'])
def path():
    CurrentPath = os.getenv("PATH")
    return str(CurrentPath)


f = open("serverParameters/PORT.txt", "w")
f.write(str(PORT))
f.close()
f = open("shutdown.txt", "w")
f.write("SHUTDOWN="+str(SHUTDOWN)+"\n")
f.close()
# PID = os.getpid()
f = open("shutdown.txt", "a")
f.write("PID="+str(PID))
f.close()

limit = -1
SHUTDOWN = int(SHUTDOWN)
if SHUTDOWN > limit:
    subprocess.Popen(["python3", "server_shutdown.py"])

app.run(host=HOST, port=PORT)
