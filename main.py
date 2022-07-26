"""
Time:       2022/07/26
Author:     Justin Hsu
Version:    V 0.1
File:       main.py
Describe: Write during DMCL after graduate, Github link: 
"""

import function as f

import pymongo
from pymongo import MongoClient

import json
import csv
import pandas as pd
import getpass


def run():
    
    #set login string
    username = password = ip = port = ""
    (username, password, ip, port) = f.getLoginInfo()
    loginStr = f.getAuthString(username, password, ip, port)

    #printDB
    f.print_dbList(loginStr)

    #create or use existing Db and Collections
    s_mydb = ""
    s_mycol = ""
    (s_mydb, s_mycol) = f.createDbAndCol(loginStr)
    print("Now using Database: '" + s_mydb  + "', Collection: '" + s_mycol + "'.")

    #set auth and db collection
    client = pymongo.MongoClient(loginStr)
    mydb = client[s_mydb]
    mycol = mydb[s_mycol]

    #insert file
    f.checkFileType(mycol)

    #end
    print("process end")


if __name__=='__main__':
    run()

