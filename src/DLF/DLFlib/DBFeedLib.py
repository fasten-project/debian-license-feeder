#!/usr/bin/python
from configparser import ConfigParser
import psycopg2
import os
import json
import time

#from config import config

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def insert_package(package_name, forge):
    """ insert a new package into the packages table """
    sql = """INSERT INTO packages(package_name, forge) VALUES(%s, %s) RETURNING id"""
    conn = None
    id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (package_name, forge,))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print("The id of "+package_name+" is: "+str(id))
    return id

def insert_package_versions(package_id, version, cg_generator):
    """ insert a new package versions into the package versions table """
    sql = """INSERT INTO package_versions(package_id, version, cg_generator) VALUES(%s, %s, %s) RETURNING id"""
    conn = None
    id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (package_id, version, cg_generator,))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    #print("The package_version id of "+package_name+" "+version+" is: "+str(id))
    return id

def retrieve_id_package(package_name):
    """ retrieve a package id from the packages table """
    sql = """select id from packages where package_name = %s"""
    conn = None
    id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (package_name,))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print("The id of "+package_name+" is: "+str(id))
    return id

def retrieve_id_package_versions(package_id, version):
    """ retrieve a package id from the package_versions table """
    sql = """select id from package_versions where package_id = %s AND version = %s """
    conn = None
    id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (package_id, version,))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print("The package versions id of the package id "+str(package_id)+", version "+ version +" is: "+str(id))
    return id

def insert_files(package_version_id, path, metadata):
    """ insert a new package into the packages table """
    sql = """INSERT INTO files(package_version_id, path, metadata) VALUES(%s, %s, %s) RETURNING id"""
    conn = None
    id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (package_version_id, path, metadata,))
        # get the generated id back
        id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print("The id of "+path+", of the package version id: "+str(package_version_id)+"  is: "+str(id))
    return id

def PopulateDB(packageName,packageVersion):
    forge = "Debian"
    cg_generator = "CScout"
    insert_package(packageName,forge)
    package_id = retrieve_id_package(packageName)
    insert_package_versions(package_id,packageVersion,cg_generator)
    package_version_id = retrieve_id_package_versions(package_id, packageVersion)
    return package_version_id


def FeedLicenseForFile(packageName,packageVersion):
    dir = "collectingDebianLicensesChecksum/"+packageName
    for (root,dirs,files) in os.walk(dir, topdown=True):
        for file in files:
            if ".json" in file:
                fname = root+"/"+file
                with open(fname, 'r') as f:
                    print(fname)
                    dict = json.load(f)
                    versions = dict['result']['copyright']
                    for i in range(len(versions)):
                        if versions[i]['version'] == str(packageVersion):
                            license = versions[i]['license']
                            currentPackagePath = fname.replace("collectingDebianLicensesChecksum/"+packageName+"/", '')
                            currentPackagePath = currentPackagePath.replace(".json",'')
                            print (currentPackagePath)
                            metadata = '{ "licenses": [{"name": "'+ license +'", "source": "Debian API"}] }'
                            print(metadata)
                            path = versions[i]['path']
                            print(path)
                            if currentPackagePath == path:
                                package_id = retrieve_id_package(packageName)
                                print("Package id is: "+str(package_id))
                                package_version_id = retrieve_id_package_versions(package_id, packageVersion)
                                print("Package version id is: "+str(package_version_id))
                                files_id = insert_files(package_version_id, path, metadata)# checksum)
                                print ("File :" +str(path)+ "has been inserted with "+str(files_id)+ " file ID")
                                time.sleep(1)
