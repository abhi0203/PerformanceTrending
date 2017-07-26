from flask import Flask, render_template,json, request
from perfResults import QueryData,comparisonData
from pymongo import MongoClient


app=Flask(__name__)


#Get Database connection, switch database, get collection handle
clientConn=MongoClient("localhost",27017)
databaseHandle=clientConn.PerformanceRegression
collectionHandle= databaseHandle.NewRelicData


#Get the data from database
condition='{"metric_data.metrics.name":"WebTransactionTotalTime"}'




@app.route("/")
def main():
	projection=json.loads('{"metric_data.metrics.timeslices.from":1,"metric_data.metrics.timeslices.values":1,"_id":0}')
	performanceMetrics=QueryData.getData(collectionHandle,"",projection)
	return render_template('index.html',data=performanceMetrics)



@app.route("/sql")
def returnSQLData():
	projection=json.loads('{"metric_data.metrics.timeslices.from":1,"metric_data.metrics.timeslices.values":1,"_id":0}')
	sqlMetrics=QueryData.getSQLData(collectionHandle,"",projection)
	return render_template('sql.html',data=sqlMetrics)

@app.route("/memory")
def returnMemoryData():
	projection=json.loads('{"metric_data.metrics.timeslices.from":1,"metric_data.metrics.timeslices.values":1,"_id":0}')
	memoryMetrics=QueryData.getMemoryData(collectionHandle,"",projection)
	return render_template('memory.html',data=memoryMetrics)


@app.route("/transaction")
def returnTransactionData():
	projection=json.loads('{"metric_data.metrics.timeslices.from":1,"metric_data.metrics.timeslices.values":1,"_id":0}')
	transactionMetrics=QueryData.getTransactionData(collectionHandle,"",projection)
	return render_template('transaction.html',data=transactionMetrics)


@app.route("/compare")
def compareResults():
	return render_template('compare.html')

@app.route("/comparisonResults", methods=['POST'])
def comparisonResults():
	before=request.form['before']
	after = request.form['after']
	projection=json.loads('{"metric_data.metrics.timeslices.from":1,"metric_data.metrics.timeslices.values":1,"_id":0}')
	comparisonDates=[]
	if not before or not after:
		return "The dates are empty"
	else:
		comparisonDates.append(before)
		comparisonDates.append(after)
		comparisonMetrics= comparisonData.getData(collectionHandle,comparisonDates,projection)
		return render_template('comparisonResults.html', data=comparisonMetrics)

if __name__=="__main__":
	app.run(host='0.0.0.0',threaded=True)