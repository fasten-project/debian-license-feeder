import sys
from dotenv import load_dotenv
from os import environ, path
import os
import requests
import json
import time
import sys
import pandas as pd
import numpy as np
import re
import fileinput

'''
* SPDX-FileCopyrightText: 2021 Michele Scarlato <michele.scarlato@endocode.com>
*
* SPDX-License-Identifier: MIT
'''

#packageName = "0ad"
packageVersion = "latest"
debianVersion = "bullseye"


def RetrievePackageFilesAndDirectory(packageName, packageVersion):
    print("https://sources.debian.org/api/src/"+packageName+"/"+packageVersion+"/")
    try:
        try:
            response = requests.get("https://sources.debian.org/api/src/"+packageName+"/latest/", timeout=10)
            time.sleep(1.2)
            if response.status_code == 200:
                jsonResponse=response.json()
                with open('collectingDebianLicenses/'+packageName+'/'+packageName+'_pkg.json', 'w', encoding='utf-8') as f:
                    print("writing file")
                    json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                return jsonResponse
            else:
                jsonResponse = "404"
                return jsonResponse
        except requests.exceptions.ConnectionError:
            requests.status_code = "Connection refused"

    except requests.exceptions.ReadTimeout:
        print ("Timeout occurred")


def CreateDirectory(root,directory):
    path = os.path.join(root, directory)
    print("Inside create directory:")
    print("root :"+root)
    print("directory :"+directory)
    print("path :"+path)
    try:
        os.makedirs(path, exist_ok = True)
        print("Directory '%s' created successfully" % directory)
        #print(path)
        return path
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

def RetrieveFilesInfo(packageName,packageVersion,path):
    fileName = path
    path = packageName+"/"+packageVersion+"/"+path
    #print(path)
    print("https://sources.debian.org/api/src/"+path+"/")
    try:
        try:
            #page1 = requests.get(ap)
            response = requests.get("https://sources.debian.org/api/src/"+path+"/", timeout=10)
            time.sleep(1.2)
            if response.status_code == 200:
                jsonResponse=response.json()
                #print(jsonResponse)
                with open('collectingDebianLicenses/'+packageName+'/'+fileName+'.json', 'w', encoding='utf-8') as f:
                    json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                return jsonResponse
            else:
                jsonResponse = "404"
                output = jsonResponse+", 404 - page not found"
                #print(output)
                #appendToFile(output)
                return output
        except requests.exceptions.ConnectionError:
            requests.status_code = "Connection refused"
    except requests.exceptions.ReadTimeout:
        print ("Timeout occurred")

def RetrieveDirectoryInfo(packageName,packageVersion,path):
    #print("Inside of DirectoryInfo")
    directory = path
    path = packageName+"/"+packageVersion+"/"+path
    print("https://sources.debian.org/api/src/"+path+"/")
    try:
        try:
            #page1 = requests.get(ap)
            response = requests.get("https://sources.debian.org/api/src/"+path+"/", timeout=10)
            time.sleep(1.2)
            if response.status_code == 200:
                print("status code 200")
                jsonResponse=response.json()
                #print(jsonResponse)
                fname = 'collectingDebianLicenses/'+packageName+"/"+directory+"/"+directory+'_dir.json'
                # this control is required to scan nested directories
                #if os.path.isfile(fname):
                #if os.path.isfile(fname):
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                    return jsonResponse
            else:
                jsonResponse = "404"
                output = jsonResponse+", 404 - page not found"
                return output
        except requests.exceptions.ConnectionError:
            requests.status_code = "Connection refused"
    except requests.exceptions.ReadTimeout:
        print ("Timeout occurred")




def RetrieveDirectoryInfoNotRecursive(packageName,packageVersion,path):
    #print("Inside of DirectoryInfo")
    directory = path
    print(directory)
    fileName = path
    fileName = fileName.replace("/"," ")
    fileNameList = fileName.split()
    #print(fileNameList)
    fileName = fileNameList[-1]
    #print(fileName)
    path = packageName+"/"+packageVersion+"/"+path
    print("https://sources.debian.org/api/src/"+path+"/")
    try:
        try:
            #page1 = requests.get(ap)
            response = requests.get("https://sources.debian.org/api/src/"+path+"/", timeout=10)
            time.sleep(1.2)
            if response.status_code == 200:
                print("status code 200")
                jsonResponse=response.json()
                #print(jsonResponse)
                fname = 'collectingDebianLicenses/'+packageName+"/"+directory+"/"+fileName+'_dir.json'
                # this control is required to scan nested directories
                #if os.path.isfile(fname):
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                    root = 'collectingDebianLicenses/'+packageName+'/'+directory
                    jsonFile = fileName+'_dir.json'
                    print(root)
                    print(jsonFile)
                ScanJsonDir(packageName,packageVersion,root,jsonFile)
                return jsonResponse
            else:
                jsonResponse = "404"
                output = jsonResponse+", 404 - page not found"
                return output
        except requests.exceptions.ConnectionError:
            requests.status_code = "Connection refused"
    except requests.exceptions.ReadTimeout:
        print ("Timeout occurred")


def ScanJsonDir(packageName,packageVersion,root,jsonFile):
    fname = root+"/"+jsonFile
    print("Fname is:")
    print(fname)
    #print(os.path.isfile(fname))
    #print("inside dir.json and pkg.json loop")
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            print("Opening file")
            print(fname)
            #print(f)
            currentPath = os.getcwd()
            print("Current Path:")
            print(currentPath)
            #if fname == None or f == '':
            #    print('I got a null or empty string value for data in a file')
            if f == None or f == '':
                print("this file is empty")
            else:
                dict = json.load(f)
                #print(dict)
                if "content" in dict:
                    subDict = dict["content"]
                    for item in subDict:
                        if item["type"] == "directory":
                            directory = item["name"]
                            path = root + "/" + directory
                            print("This is the path of a directory found in the :"+ path)
                            print(path)
                            if "//" in path:
                                path = path.replace("//","/")
                                print("ModPath:")
                                print(path)
                            if not os.path.isdir(path):
                                path = CreateDirectory(root,directory)
                                path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                                print (path)
                                print ("Inside of type directory in ScanJsonDir")
                                time.sleep(1.2)
                                RetrieveDirectoryInfoNotRecursive(packageName,packageVersion,path)
                            else:
                                print("Directory already exist")
                        if item["type"] == "file":
                            fileName = item["name"]
                            path = root+"/"+fileName
                            print("This is the path of a file found in the :"+ path)
                            print(path)
                            if "//" in path:
                                path = path.replace("//","/")
                                print("ModPath:")
                                print(path)
                            if not os.path.isfile(path+".json"):
                                #print(fileName)
                                #print(root)
                                path = path.replace("collectingDebianLicenses/"+packageName+"/","")
                                print("Path generated inside of ScanJsonDir for FILE type")
                                print(path)
                                RetrieveFilesInfo(packageName,packageVersion,path)
                            else:
                                print("File already exist")
# currently not used
def ScanJsonFile(packageName,root,jsonFile):
    print("this is from inside ScanJsonFile")
    return

def ScanJsonDirChecksum(root,packageName,jsonFile):
    fname = root+"/"+jsonFile
    print(fname)
    directory = root.replace("collectingDebianLicenses/"+packageName+"/","")
    if "//" in fname:
        fname = fname.replace("//","/")
        print(fname)
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            print("Opening file")
            print(fname)
            dict = json.load(f)
            if "checksum" in dict:
                checksum = dict["checksum"]
                try:
                    try:
                        #page1 = requests.get(ap)
                        if checksum != "":
                            response = requests.get("https://sources.debian.org/copyright/api/sha256/?checksum="+str(checksum)+"&package="+str(packageName), timeout=10)
                            print("https://sources.debian.org/copyright/api/sha256/?checksum="+str(checksum)+"&package="+str(packageName))
                            if response.status_code == 200:
                                print("status code 200")
                                jsonResponse=response.json()
                                fname = fname.replace("collectingDebianLicenses","collectingDebianLicensesChecksum")
                                with open(fname, 'w', encoding='utf-8') as f:
                                    json.dump(jsonResponse, f, ensure_ascii=False, indent=4)
                                print(jsonResponse)
                                print("\n\n\n")

                                return jsonResponse
                            else:
                                jsonResponse = "404"
                                output = jsonResponse+", 404 - page not found"
                                return output
                    except requests.exceptions.ConnectionError:
                        requests.status_code = "Connection refused"

                except requests.exceptions.ReadTimeout:
                    print ("Timeout occurred")
                #time.sleep(1.2)


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


# currently not used

def RetrieveChecksum(path):
    return checksum
