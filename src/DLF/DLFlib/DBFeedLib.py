#!/usr/bin/python
from configparser import ConfigParser
import psycopg2
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
    print("The package_version id of "+package_name+" "+version+" is: "+str(id))
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

def insert_files(package_version_id, path, checksum):

    """ insert a new package into the packages table """
    sql = """INSERT INTO files(package_version_id, path, checksum) VALUES(%s, %s, %s) RETURNING id"""
    conn = None
    id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (package_version_id, path, checksum,))
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
