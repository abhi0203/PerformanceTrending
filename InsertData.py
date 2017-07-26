from pymongo import MongoClient
from pprint import pprint
import datetime
import sys
import ast

def insertData(collectionHandle,data):
	insertID= collectionHandle.insert_one(data)
	return insertID

#Get Database connection, switch database, get collection handle
clientConn=MongoClient("localhost",27017)
databaseHandle=clientConn.PerformanceRegression
collectionHandle= databaseHandle.NewRelicData

#Prepare the data for insertion.
data=ast.literal_eval(sys.argv[1])
insertID=insertData(collectionHandle,data)
assert insertID != None, "Something wrong with insertion"