from pymongo import MongoClient
from pprint import pprint
import json
import datetime
import sys
import ast


def insertData(collectionHandle,data):
	insertID= collectionHandle.insert_one(data)
	return insertID



def getData(collectionHandle,condition):
	'''for data in collectionHandle.find():
		pprint(data)
	'''
	print("Got a call")
	performanceMetrics={}
	webTransactionResponseTime=[]
	webTransactionRPM=[]
	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"WebTransactionTotalTime"},{"metric_data.metrics.timeslices.from":1,"metric_data.metrics.timeslices.values":1,"_id":0}):
		dateString= dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		#Changes by Abhiram		
		dateValue=datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b')
		dateValue=datetime.datetime.strptime(dateValue,'%d-%b')
		if 'average_response_time' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			responseTimeValue=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['average_response_time']
			webTransactionResponseTime.append([dateValue,responseTimeValue])
		elif 'requests_per_minute' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			requestPerMinValue=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['requests_per_minute']
			webTransactionRPM.append([dateValue,requestPerMinValue])
		#print(webTransactionResponseTime)
	
	performanceMetrics['webTransactionResponseTime']=webTransactionResponseTime
	performanceMetrics['webTransactionRPM']=webTransactionRPM
	return performanceMetrics
	
