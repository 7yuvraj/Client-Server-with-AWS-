import requests
import json
from requests.models import PreparedRequest
import pprint
from random import seed
from random import randint
from tkinter import*
window=Tk()
window.geometry('500x500')
l1 = Label(window, text="Fetch Data from Server")
l2 = Label(window, text="------------------")


#generate and print user Request for Work ID
url_t = 'http://flaskserver-env.eba-xiaxqwwi.ca-central-1.elasticbeanstalk.com/user_id'
op = requests.get(url_t)
RFWID = op.json()['User_ID']
l3 = Label(window, text="Request ID: {}".format(RFWID))
l1.pack()
l2.pack()
l3.pack()

# User Input to select the File type
l4 = Label(window, text="Select the file type")
l4.pack()
bench=StringVar()
bench.set("DVD-testing")
selectfile= OptionMenu(window, bench, "DVD-testing","DVD-training","NDBench-testing","NDBench-training")
selectfile.pack(pady=20)


# User Input to select WorkLoad Metric
l5 = Label(window, text="Select the work load type")
l5.pack()
work=StringVar()
work.set("CPUUtilization_Average")
select_work=OptionMenu(window, work,"CPUUtilization_Average","NetworkIn_Average","NetworkOut_Average","MemoryUtilization_Average")
select_work.pack(pady=20)


#User Input to select the data range
batchUnit= IntVar()
l7 = Label(window, text="Enter samples in one batch: ")
l7.pack()
mybox=Entry(textvariable=batchUnit)
mybox.pack(pady=10)


batchID=IntVar()
l8 = Label(window, text="Enter Batch ID: ")
l8.pack()
mybox1=Entry(textvariable=batchID)
mybox1.pack(pady=10)


batchSize=IntVar()
l9 = Label(window, text="Enter Batch Size: ")
l9.pack()
mybox2=Entry(textvariable=batchSize)
mybox2.pack(pady=10)
    	
pretty=pprint.PrettyPrinter()
def reqedata():
	#appending JSON with the URL
	# 	url for EC2
	url = 'http://flaskserver-env.eba-xiaxqwwi.ca-central-1.elasticbeanstalk.com/reqData?'
	#	url for local host
	#url = 'http://127.0.0.1:5000/reqData?'
	para = {'RFWID':RFWID,'bench_type':bench.get(),'metric':work.get(),'batchUnit':batchUnit.get(),'batchID':batchID.get(),'batchSize':batchSize.get()}
	
	req = PreparedRequest()
	req.prepare_url(url,para)
	rep = requests.get(req.url)
	#print(req.url)
	if rep.status_code == 200: 
		print("\n Response from Server is ")
		pretty.pprint(rep.json())

		print("\nData:\n",rep.json()['DATA'])
		print("\nRFWID:\n",rep.json()['ID'])
		print("\nLastBatchID:\n",rep.json()['LastBatchID'])
		with open('data.json', 'w') as outfile:
				json.dump(rep.json(), outfile)
	else:
		print("HTTP Error")

mybutton=Button(window,text="Fetch Data", command= reqedata)
mybutton.pack(pady=10)


window.mainloop()