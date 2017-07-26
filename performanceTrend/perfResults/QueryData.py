from pymongo import MongoClient
from pprint import pprint
import json
import datetime
import sys
import ast


def insertData(collectionHandle,data):
	insertID= collectionHandle.insert_one(data)
	return insertID



def getData(collectionHandle,condition,projection):
	'''for data in collectionHandle.find():
		pprint(data)
	'''
	performanceMetrics={}
	webTransactionResponseTime=[]
	webTransactionRPM=[]
	platformCPUUtilization=[]
	dbCPUUtilization=[]
	indexCount=0


	#Code to get the response time and throughput stats.
	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"WebTransactionTotalTime"},projection).sort([("metric_data.from",1)]):
		dateString= dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		#Changes by Abhiram		
		dateValue=datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		#dateValue=datetime.date
		if 'average_response_time' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			responseTimeValue=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['average_response_time']
			webTransactionResponseTime.append([dateValue,responseTimeValue])
		elif 'requests_per_minute' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			requestPerMinValue=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['requests_per_minute']
			webTransactionRPM.append([dateValue,requestPerMinValue])

	#code to get the CPU stats for platform
	#reset the index count
	indexCount=0

	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"CPU_User_Utilization"},projection).sort([("metric_data.from",1)]):
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

	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"System_CPU_User_percent"},projection).sort([("metric_data.from",1)]):
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
	performanceMetrics['webTransactionRPM']=webTransactionRPM
	performanceMetrics['platformCPUUtilization']=platformCPUUtilization
	performanceMetrics['dbCPUUtilization']=dbCPUUtilization
	#print(performanceMetrics)
	return performanceMetrics


'''Method to get the SQL data'''

def getSQLData(collectionHandle,condition,projection):
	'''for data in collectionHandle.find():
		pprint(data)
	'''
	sqlMetrics={}

	insertCount=[]
	insertResponseTime=[]

	updateCount=[]
	updateResponseTime=[]

	selectCount=[]
	selectResponseTime=[]

	deleteCount=[]
	deleteResponseTime=[]
	
	#Code to get the Call Count and Resposne Time for Insert queries
	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"Datastore_operation_MySQL_insert"},projection).sort([("metric_data.from",1)]):
		dateString= dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		#Changes by Abhiram		
		dateValue=datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		#dateValue=datetime.date
		if 'call_count' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			callCount=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['call_count']
			insertCount.append([dateValue,callCount])
		elif 'average_response_time' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			avgResponseTime=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['average_response_time']
			insertResponseTime.append([dateValue,avgResponseTime])

	
	#Code to get the Call Count and Resposne Time for Update queries
	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"Datastore_operation_MySQL_update"},projection).sort([("metric_data.from",1)]):
		dateString= dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		#Changes by Abhiram		
		dateValue=datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		#dateValue=datetime.date
		if 'call_count' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			callCount=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['call_count']
			updateCount.append([dateValue,callCount])
		elif 'average_response_time' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			avgResponseTime=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['average_response_time']
			updateResponseTime.append([dateValue,avgResponseTime])

	#Code to get the Call Count and Resposne Time for Select queries
	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"Datastore_operation_MySQL_select"},projection).sort([("metric_data.from",1)]):
		dateString= dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		#Changes by Abhiram		
		dateValue=datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		#dateValue=datetime.date
		if 'call_count' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			callCount=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['call_count']
			selectCount.append([dateValue,callCount])
		elif 'average_response_time' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			avgResponseTime=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['average_response_time']
			selectResponseTime.append([dateValue,avgResponseTime])


	#Code to get the Call Count and Resposne Time for delete queries
	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"Datastore_operation_MySQL_delete"},projection).sort([("metric_data.from",1)]):
		dateString= dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		#Changes by Abhiram		
		dateValue=datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		#dateValue=datetime.date
		if 'call_count' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			callCount=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['call_count']
			deleteCount.append([dateValue,callCount])
		elif 'average_response_time' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			avgResponseTime=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['average_response_time']
			deleteResponseTime.append([dateValue,avgResponseTime])



	sqlMetrics['insertCount']=insertCount
	sqlMetrics['insertResponseTime']=insertResponseTime


	sqlMetrics['updateCount']=updateCount
	sqlMetrics['updateResponseTime']=updateResponseTime

	sqlMetrics['selectCount']=selectCount
	sqlMetrics['selectResponseTime']=selectResponseTime


	sqlMetrics['deleteCount']=deleteCount
	sqlMetrics['deleteResponseTime']=deleteResponseTime
	return sqlMetrics


def getMemoryData(collectionHandle,condition,projection):
	'''for data in collectionHandle.find():
		pprint(data)
	'''
	memoryMetrics={}
	platformMemoryUtilization=[]
	gcScavengeUtilization=[]
	gcMarkSweepUtilization=[]

	indexCount=0


	# Code to get Memory stats
	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"Memory_Heap_Used"},projection).sort([("metric_data.from",1)]):
		dateString= dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		dateValue=datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		if 'total_used_mb' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			memoryValue=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['total_used_mb']
			if not platformMemoryUtilization:
				platformMemoryUtilization.append([dateValue,memoryValue])	
			else:
				if dateValue in platformMemoryUtilization[indexCount]:
					platformMemoryUtilization[indexCount].append(memoryValue)
				else:
					platformMemoryUtilization.append([dateValue,memoryValue])
					indexCount+=1

	
	#Code to get the GC_PS_SCAVENGE stats for database
	#reset the index count
	indexCount=0

	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"GC_PS_Scavenge"},projection).sort([("metric_data.from",1)]):
		dateString = dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		dateValue = datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		if 'utilization' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			gcScavengeValue=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['utilization']
			if not gcScavengeUtilization:
				gcScavengeUtilization.append([dateValue,gcScavengeValue])	
			else:
				if dateValue in gcScavengeUtilization[indexCount]:
					gcScavengeUtilization[indexCount].append(gcScavengeValue)
				else:
					gcScavengeUtilization.append([dateValue,gcScavengeValue])
					indexCount+=1

	#Code to get the GC_PS_MarkSweep stats for database
	#reset the index count
	indexCount=0

	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"GC_PS_MarkSweep"},projection).sort([("metric_data.from",1)]):
		dateString = dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']		
		dateValue = datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		if 'utilization' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			gcMarkSweepValue=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['utilization']
			if not gcMarkSweepUtilization:
				gcMarkSweepUtilization.append([dateValue,gcMarkSweepValue])	
			else:
				if dateValue in gcMarkSweepUtilization[indexCount]:
					gcMarkSweepUtilization[indexCount].append(gcMarkSweepValue)
				else:
					gcMarkSweepUtilization.append([dateValue,gcMarkSweepValue])
					indexCount+=1
	

	memoryMetrics['platformMemoryUtilization']=platformMemoryUtilization
	memoryMetrics['gcScavengeUtilization']=gcScavengeUtilization
	memoryMetrics['gcMarkSweepUtilization']=gcMarkSweepUtilization
	#print(memoryMetrics)
	return memoryMetrics


def getTransactionData(collectionHandle,condition,projection):
	'''This method is created to get the transaction relatd data from New Relic.'''
	transactionMetrics={}
	
	gwtTransactionResponseTime=[]
	gwtTransactionRPM=[]

	restletTransactionResponseTime=[]
	restletTransactionRPM=[]

	# Get the GWT transaction Data
	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"WebTransaction_Servlet_Key[type=com.boomi.platform.gwt.framework.ClientRequestTrackerServiceServlet,_annotation=[none]]"},projection).sort([("metric_data.from",1)]):
		dateString=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']
		dateValue= datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		if 'average_response_time' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			gwtResponseTime=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['average_response_time']
			gwtTransactionResponseTime.append([dateValue,gwtResponseTime])
		elif 'requests_per_minute' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			gwtRPM = dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['requests_per_minute']
			gwtTransactionRPM.append([dateValue,gwtRPM])


	# Get the Restlet transaction Data
	for dataCursor in collectionHandle.find({"metric_data.metrics.name":"WebTransactionTotalTime_Servlet_RestletServlet"},projection).sort([("metric_data.from",1)]):
		dateString=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['from']
		dateValue= datetime.datetime.strptime(dateString,"%Y-%m-%dT%H:%M:%S+00:00").strftime('%d-%b-%Y')
		if 'average_response_time' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			restletResponseTime=dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['average_response_time']
			restletTransactionResponseTime.append([dateValue,restletResponseTime])
		elif 'requests_per_minute' in dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']:
			restletRPM = dataCursor['metric_data']['metrics'][0]['timeslices'][0]['values']['requests_per_minute']
			restletTransactionRPM.append([dateValue,restletRPM])
	

	transactionMetrics['gwtTransactionResponseTime']=gwtTransactionResponseTime
	transactionMetrics['gwtTransactionRPM']=gwtTransactionRPM
	transactionMetrics['restletTransactionResponseTime']=restletTransactionResponseTime
	transactionMetrics['restletTransactionRPM']=restletTransactionRPM

	return transactionMetrics