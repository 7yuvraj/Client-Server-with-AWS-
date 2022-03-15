from flask import Flask, render_template, request
import json
import pandas as pd
from random import seed 
from random import randint
seed(1)
application = Flask(__name__)

@application.route('/')
def index():
	return 'Welcome, The Server is running on AWS EC2 instance and the data is being fetched from S3 Bucket'

#To generate User ID and save in S3
@application.route("/user_id")
def user():
    user_id = randint(1000,9999)
    return json.dumps({"User_ID":user_id})



@application.route("/reqData")
def req():

    RFWID = int(request.args.get("RFWID"))
    bench_type=request.args.get("bench_type")
    metric= request.args.get("metric")
    batchUnit=int(request.args.get("batchUnit"))
    batchID=int(request.args.get("batchID"))
    batchSize= int(request.args.get("batchSize"))
# from git
    #coloumn = pd.read_csv(
       # "https://raw.githubusercontent.com/haniehalipour/Online-Machine-Learning-for-Cloud-Resource-Provisioning-of-Microservice-Backend-Systems/master/Workload%20Data/" + bench_type + ".csv")

# from S3 bucket    
    coloumn = pd.read_csv('https://1assignmentdata1.s3.ca-central-1.amazonaws.com/'+ bench_type + ".csv")

    respData = []
    for i in range(batchSize):
        startBatch = (batchUnit* (batchID+i-1))
        endBatch = (batchUnit* (batchID+i))
        if endBatch >=len(coloumn):
            endBatch=len(coloumn)
            respData.append(((coloumn[metric][startBatch:endBatch]).values).tolist())
            lastbatch = batchID+i
            break
        
        else:
            respData.append(((coloumn[metric][startBatch:endBatch]).values).tolist())
            lastbatch = batchID+i
    return(json.dumps({'ID':RFWID,'LastBatchID':lastbatch,'DATA': respData}))

if __name__ == "__main__":
	application.run()