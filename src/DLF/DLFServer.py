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


@app.route('/DebianPackageVersion', methods=['POST', 'GET'])
def GetDebianPackageVersion():
    print("Hola")
    args = request.args
    packageNameAndVersion = args['packageNameAndVersion']
    packageNameAndVersion = packageNameAndVersion.split(",")
    packageName = packageNameAndVersion[0]
    packageVersion = packageNameAndVersion[1]
    print(packageName)
    print(packageVersion)
    DebianChecksumCollector(packageName,packageVersion)
    DebianLicenseCollector(packageName,packageVersion)
    output = "Elaborating "+packageName+", version "+packageVersion+" ... "
    return output



def DebianChecksumCollector(packageName,packageVersion):
    parent_dir = "collectingDebianLicenses"
    dir = "collectingDebianLicenses/"+packageName
    print("Inside Debian License Collector function in the server")
    #If the directory doesn't exist, create it and scan the package.
    if not os.path.isdir(dir):
        CreateDirectory(parent_dir,packageName)
        RetrievePackageFilesAndDirectory(packageName,packageVersion)
    #parse davfs2_pkg.json
    print (packageName+"_pkg.json")
    ScanJsonDir(packageName,packageVersion,dir,packageName+"_pkg.json")
    """
    #this loop create the first layer of files and directories
    for (root,dirs,files) in os.walk(dir, topdown=True):
        if not os.listdir(root):
            print("This is an empty dir")
            root = root.replace("collectingDebianLicenses/"+packageName+"/","")
            print("here root is:")
            print(root)
            RetrieveDirectoryInfoNotRecursive(packageName,root)
        for directory in dirs:
            print(".. looping through directory ..: " +root+directory)
            for file in os.listdir(root+"/"+directory):
                if not os.listdir(root+"/"+directory):
                    print("This is an empty dir")
                    RetrieveDirectoryInfo(packageName,root+"/"+directory)
                else:
                    for file in os.listdir(root+"/"+directory):
                        print("Inside "+directory+" there is :"+file)
        for file in files:
            print(".. looping through files .. " +file)
            if "_dir.json" in file:
                path = dir
                path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                print(path)
                ScanJsonDir(packageName,root+"/",file)
                time.sleep(0.2)
    """

def DebianLicenseCollector(packageName,packageVersion):
    parent_dir = "collectingDebianLicenses"
    dir = "collectingDebianLicenses/"+packageName
    parent_dirChecksum = "collectingDebianLicensesChecksum/"+packageName
    #If the directory doesn't exist, create it and scan the package.
    if not os.path.isdir(parent_dirChecksum):
        print("creating directory")
        CreateDirectory(parent_dirChecksum,packageName)
    else:
        print(parent_dirChecksum+" already exists")
    #ScanJsonDirChecksum(dir,packageName,)
    #this loop creates the first layer of files and directories
    for (root,dirs,files) in os.walk(dir, topdown=True):
        for file in files:
            print(".. looping through files .. " +file)
            if "_dir.json" in file or "_pkg.json" in file:
                print("this is not json of a file" )
                continue
            if ".json" in file:
                path = dir
                pathChecksum = root.replace("collectingDebianLicenses","collectingDebianLicensesChecksum")
                pathChecksum = pathChecksum+"/"+file
                print(pathChecksum)
                if not os.path.isfile(pathChecksum):
                    path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                    print("Running ScanJsonDirChecksum upon :"+root+"/"+file)
                    ScanJsonDirChecksum(root,packageName,file)
                    time.sleep(1.2)
        for directory in dirs:
            print(root)
            print(dirs)
            print(".. looping through directory ..: " +root+"/"+directory)
            rootCheckusm = root.replace("collectingDebianLicenses","collectingDebianLicensesChecksum/")
            if not os.path.isdir(rootCheckusm+"/"+directory):
                print("creating directory:"+rootCheckusm+"/"+directory)
                CreateDirectory("",rootCheckusm+"/"+directory)
            for file in os.listdir(root+"/"+directory):
                if "_dir.json" in file or "_pkg.json" in file:
                    print(file+" is not json of a file" )
                    continue
                if ".json" in file:
                    path = dir
                    pathChecksum = root.replace("collectingDebianLicenses","collectingDebianLicensesChecksum")
                    pathChecksum = pathChecksum+"/"+directory+"/"+file
                    print(pathChecksum)
                    if not os.path.isfile(pathChecksum):
                        path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                        print("Running ScanJsonDirChecksum upon :"+root+"/"+directory+"/"+file)
                        ScanJsonDirChecksum(root+"/"+directory,packageName,file)
                        time.sleep(1.2)




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
