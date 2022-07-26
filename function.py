import pymongo
from pymongo import MongoClient

import json
import csv
import pandas as pd
import getpass

#print all the database in mongodb
def print_dbList(loginStr):
    print("Existing database list:")
    print_db_admin = pymongo.MongoClient(loginStr)
    i = 1
    for db in print_db_admin.list_databases():
        if str(db["name"]) != "admin":
            if str(db["name"]) != "config":
                print(str(i) + "." + db["name"], end='\n')
                i += 1

#confirm authorize
def getLoginInfo():
    this_username = input("Username: ")
    this_password = getpass.getpass("Password: ")
    this_ip = input("IP: ")
    this_port = input("Port: ")

    return (this_username, this_password, this_ip, this_port)


#check Database input
def checkDB(inputDB, loginStr):
    print_db_admin = pymongo.MongoClient(loginStr)
    if inputDB == "new":
        return True
    else:
        for db in print_db_admin.list_databases():
            if(str(inputDB) == str(db["name"])):
                return True
        return False

#check collection
def checkCollection(dbName, inputCol):
    for col in range(len(dbName.list_collection_names())):
        if(str(inputCol) == dbName.list_collection_names()[col]):
            print("Collection found: " + str(dbName.list_collection_names()[col]) + "!!")
            return False
    return True

#create or use old db and collection
def createDbAndCol(loginStr):
    dbName = colName = ""

    client2 = pymongo.MongoClient(loginStr)
    mydb = client2['admin']
    setDatabase = input(str(" Type 'new' to create new database \n or type existing database: ") )

    #check input
    checkdb = checkDB(setDatabase, loginStr) #return boolean
    while checkdb != True:
        setDatabase = input(str("input error, please enter 'new' or existing database!!\n"))
        checkdb = checkDB(setDatabase, loginStr)
        print_dbList(loginStr)
        
    #create new database
    if setDatabase == "new":
        dbName = input(str("Please enter new databaseName: "))
        ##db = client2[dbName]
        
        #Sharding or not
        # enableShard = input(str("Do you want to enable sharding in this database? \n[y/n]: "))
        # while enableShard != 'y' or enableShard != 'n':
        #     if enableShard == "y":
        #         print("sharding enabled!") ###
        #         #db_admin.command('enableSharding', dbName)
        #     elif enableShard == 'n':
        #         print("sharding disabled!")
        #         break
        #     else:
        #         enableShard = input(str("Please enter 'y' or 'n' to confirm !!\n[y/n]: "))

        #create new collection
        dbCollection = input(str("Please enter a name under database " + dbName +"'s Collection :"))
        colName = dbCollection
        ##collection = db[dbCollection]

    # use existing database
    else :
        dbName = setDatabase
        print("using existing database '" + dbName  +"'")
        ##client2 = pymongo.MongoClient(loginStr)
        mydb = client2[dbName]

        #create or use old collection
        print(mydb.list_collection_names())
        colName = input("Please enter a new name to create Collection or use existing one above: ")
        CreateNewCol = checkCollection(mydb, colName)
        print(CreateNewCol)
        if (CreateNewCol == False):
            print("Using existing collection!")
            colName = colName ###
        else:
            print("creating new collection!")
            print(colName + " is created!")
            colName = colName

    return (dbName, colName)


#check inserting Json or CSV file
def checkFileType(mycol):
    JorC = input("Enter j for 'json' file and c for 'csv' file: ")
    while( JorC != 'j' or JorC != 'c'):
        if(JorC == 'j'):
            break
        elif(JorC=='c'):
            break
        else:
            print("Input error")
            JorC = input("Enter j for 'json' file and c for 'csv' file: ")
            
    if(JorC == 'j'):
        print("Inserting json file...")
        insertJson(mycol)
    if(JorC == 'c'):
        print("Inserting csv file...")
        insertCsv(mycol)

#insert json file
def insertJson(mycol):
    isDir = input("Is the file under same directory? [y/n]: ")
    if( isDir == 'y'):
        print("Json file is under same directory.")
        dir = input("Please enter file name ( .json is not needed ): ")
        datapath = "./" + dir + ".json"
        print(datapath)
        try:
            with open( datapath,'r', encoding="utf-8") as f:
                file_data = json.load(f)
            mycol.insert_many(file_data)
            print("File inserted!!")

        except:
            print("insert failed...")
            print( "returning to filetype check...")
            checkFileType(mycol)

    elif ( isDir == 'n'):
        print("Json file is not under same directory.")
        dir = input("Please enter full path name ( .json is not needed ): \n")
        datapath = dir + ".json"
        print(datapath)
        try:
            with open( datapath,'r', encoding="utf-8") as f:
                file_data = json.load(f)
            mycol.insert_many(file_data)
            print("File inserted!!")

        except:
            print("insert failed...")
            print( "returning to filetype check...")
            checkFileType(mycol) 

    else:
        print( "returning to filetype check...")
        checkFileType(mycol)
    

#insert csv file
def insertCsv(mycol):
    isDir = input("Is the file under same directory? [y/n]: ")
    if( isDir == 'y'):
        print("Csv file is under same directory.")
        dir = input("Please enter file name ( .csv is not needed ): ")
        datapath = "./" + dir + ".csv"
        print(datapath)
        try:
            data = pd.read_csv( datapath ,encoding = 'UTF-8')
            data_json = json.loads(data.to_json(orient='records'))
            mycol.insert_many(data_json)
            print("File inserted!!")
        except:
            print("insert failed...")
            print( "returning to filetype check...")
            checkFileType(mycol)

    elif ( isDir == 'n'):
        print("Csv file is not under same directory.")
        dir = input("Please enter full path name ( .csv is not needed ): \n")
        datapath = dir + ".csv"
        print(datapath)
        try:
            data = pd.read_csv( datapath ,encoding = 'UTF-8')
            data_json = json.loads(data.to_json(orient='records'))
            mycol.insert_many(data_json)
            print("File inserted!!")

        except:
            print("insert failed...")
            print( "returning to filetype check...")
            checkFileType(mycol)
        
    else:
        print( "returning to filetype check...")
        checkFileType(mycol)



#auth information
def getAuthString(username, password, ip, port):
    Stringlogin = "mongodb://" + username + ":" + password + "@" + ip + ":" + port + "/?authMechanism=DEFAULT"
    return Stringlogin