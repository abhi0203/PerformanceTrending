from pymongo import MongoClient
from pprint import pprint
import json
import datetime
import sys
import ast


def getData(collectionHandle,comparisonDates,projection):
	'''for data in collectionHandle.find():
		pprint(data)
	'''
	performanceMetrics={}
	webTransactionResponseTime=[]
	platformCPUUtilization=[]
	dbCPUUtilization=[]
	indexCount=0


	#Code to get the response time and throughput stats.
	for dataCursor in collectionHandle.find({"$and":[{"metric_data.metrics.name":"WebTransactionTotalTime"},{"metric_data.from": {"$in":[comparisonDates[0],comparisonDates[1]]}}]},projection).sort([("metric_data.from",1)]):
		dateString= dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		#Changes by Abhiram		
		dateValue=datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		#dateValue=datetime.date
		if 'average_response_time' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			responseTimeValue=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['average_response_time']
			webTransactionResponseTime.append([dateValue,responseTimeValue])

	#code to get the CPU stats for platform
	#reset the index count

	
	indexCount=0

	for dataCursor in collectionHandle.find({"$and":[{"metric_data.metrics.name":"CPU_User_Utilization"},{"metric_data.from": {"$in":[comparisonDates[0],comparisonDates[1]]}}]},projection).sort([("metric_data.from",1)]):
		dateString= dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		dateValue=datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		if 'percent' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			cpuValue=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['percent']
			if not platformCPUUtilization:
				platformCPUUtilization.append([dateValue,cpuValue])	
			else:
				if dateValue in platformCPUUtilization[indexCount]:
					platformCPUUtilization[indexCount].append(cpuValue)
				else:
					platformCPUUtilization.append([dateValue,cpuValue])
					indexCount+=1
	
	
	#Code to get the CPU stats for database
	#reset the index count

	
	indexCount=0

	for dataCursor in collectionHandle.find({"$and":[{"metric_data.metrics.name":"System_CPU_User_percent"},{"metric_data.from": {"$in":[comparisonDates[0],comparisonDates[1]]}}]},projection).sort([("metric_data.from",1)]):
		dateString = dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		dateValue = datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		if 'average_value' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			dbcpuValue=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['average_value']
			if not dbCPUUtilization:
				dbCPUUtilization.append([dateValue,dbcpuValue])	
			else:
				if dateValue in dbCPUUtilization[indexCount]:
					dbCPUUtilization[indexCount].append(dbcpuValue)
				else:
					dbCPUUtilization.append([dateValue,dbcpuValue])
					indexCount+=1


	
	
	performanceMetrics['webTransactionResponseTime']=webTransactionResponseTime
	performanceMetrics['platformCPUUtilization']=platformCPUUtilization
	performanceMetrics['dbCPUUtilization']=dbCPUUtilization
	#print(performanceMetrics)
	return performanceMetrics