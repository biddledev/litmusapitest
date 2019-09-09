"""
PREP: Reviewed Python documentation regarding "Requests". Reviewed Litmus Preview API documentation and determined steps needed. 
Created base plan for completion of test: Create request, send email to unique InboxGuid@ email address to start test,
Verify the test is in progress. Process results and write to text file at the end. 
"""

#import modules needed for the script.
import datetime
import time
import json
import requests


#Alternative method for holding API Key and Password would be a configuaration file or command line argument. 
apikey = '*interview api key goes here*'
apipass = '*interview api password goes here*'

'''
#Could include if/else logic to stop if bad status code and display status code. Continue if 200.
response = requests.get('https://previews-api.litmus.com/Documentation/Apis')
print(response.status_code)
(commented out after determining funcitonailty)
'''

headers = {
    'Content-type': 'application/json'
}

data = '{}'

response = requests.post('https://previews-api.litmus.com/api/v1/EmailTests', headers=headers, data=data, auth=(apikey, apipass))
#print(response) - (commented out, used to test )
#print(response.status_code) - (commented out, used to test )
#print(response.text) - (commented out, used to test )

parsed_response = json.loads(response.text)

#Defining the variables "inboxguid" and "id" early on to reference later but also allow it to change accordingly in the below script. It also prints it in the terminal for ease of access.
inboxguid = str(parsed_response["InboxGuid"])
id = str(parsed_response["Id"])
print(inboxguid)
print(id)

"""Regarding the three parts of the script that involve writing to specific files "recenttests, currentstatus, and finalresuts. This was suggested by my brother
   after I had him review my code. He walked me through it but I am comfortable with the idea and implementation now. 
"""

#After pulling the id and inboxguid this writes the two variables in a text file to later reference if needed. It lists data/time as well. 
f = open("recenttests.txt", "a")
f.write("\n For test created at: " + str(datetime.datetime.now()) + "; InboxGuid:" + inboxguid + "  Id: " + id)
f.close()


#The below is used to determine the current status of our request.
response = requests.get('https://previews-api.litmus.com/api/v1/EmailTests/' + id, auth=(apikey, apipass))
#print(response.text) - (commeneted out, used to determine functionality)
parsed_response = json.loads(response.text)
print(parsed_response['State'])


"""
The below code uses while/if statements to determine and respond to the current status of our request.
Every 30 seconds it uses a GET request to find the current status and prints out a response based on the current status. 
"""
while(parsed_response["State"] == "waiting"):
   time.sleep(30)
   response = requests.get('https://previews-api.litmus.com/api/v1/EmailTests/' + id, auth=(apikey, apipass))
   parsed_response = json.loads(response.text)
   print(parsed_response["State"])
   print("Litmus is waiting for you to submit an email for testing; please send an email to " + inboxguid + "@emailtests.com")

print('done waiting')

#While the response is in "processing" it will update a text file created in the directory of the .py file with the current status of all Mobile Devices. First stating their direct status and then listing the JSON below each. 

while(parsed_response["State"] == "processing"):
   time.sleep(30)
   response = requests.get('https://previews-api.litmus.com/api/v1/EmailTests/' + id, auth=(apikey, apipass))
   parsed_response = json.loads(response.text)
   print(parsed_response["State"])
   print("Still processing; wait longer. Sorry mate")
   results_response = requests.post('https://previews-api.litmus.com/api/v1/EmailTests', headers=headers, data=data, auth=(apikey, apipass))
   results_response = json.loads(results_response.text)
   f2 = open("currenttestresults.txt", "w")
   f2.write("Current mobile test results: \n")
   for res_object in results_response["TestingApplications"]:
      current_object = res_object["PlatformName"]
      if(current_object == "Mobile devices"):
         f2.write("-----------------------------------------------------------------\n Current Results for " + res_object["ApplicationName"] + "\n The current state is: \n " + res_object["State"] + "-----------------------------------------------\n")
         f2.write(json.dumps(res_object))
         f2.write("-----------------------------------------------\n")
   f2.close()






if(parsed_response["State"] == "complete"):
   print("You did it")



results_response = requests.post('https://previews-api.litmus.com/api/v1/EmailTests', headers=headers, data=data, auth=(apikey, apipass))
results_response = json.loads(results_response.text)
f3 = open("finaltestresults.txt", "a")
f3.write("Final mobile test results for test with InboxGuid:" + inboxguid + " and Id: " + id +"is: \n")
for res_object in results_response["TestingApplications"]:
    current_object = res_object["PlatformName"]
    if(current_object == "Mobile devices"):
        f3.write("-----------------------------------------------------------------\n Current Results for " + res_object["ApplicationName"] + "\n The current state is: \n " + res_object["State"] + "-----------------------------------------------\n")
        f3.write(json.dumps(res_object))
        f3.write("-----------------------------------------------\n")
f3.close()



'''

Here is another script to use to check the status on a previous request/test you made. 
   Simply replace the Id with the test you would like to check the status of (which are auto listed with date/time 
   in the recenttest.txt ).


import datetime
import time
import json
import requests


apikey = 'interview-api'
apipass = 'interviewapipassword'

headers = {
    'Content-type': 'application/json'
}

data = '{}'



#In the below two urls you can change the {id} field to whatever ID you would like to check teh status of.

response = requests.get('https://previews-api.litmus.com/api/v1/EmailTests/{id}', auth=(apikey, apipass))
parsed_response = json.loads(response.text)
print(parsed_response['State'])

while(parsed_response["State"] == "processing"):
   time.sleep(30)
   response = requests.get('https://previews-api.litmus.com/api/v1/EmailTests/{id}', auth=(apikey, apipass))
   parsed_response = json.loads(response.text)
   print(parsed_response["State"])
   print("Still processing; wait longer. sorry mate")

if(parsed_response["State"] == "complete"):
   print("You did it")

results_response = requests.post('https://previews-api.litmus.com/api/v1/EmailTests', headers=headers, data=data, auth=(apikey, apipass))
results_response = json.loads(results_response.text)
f3 = open("finaltestresults.txt", "a")
f3.write("Final mobile test results for test with InboxGuid:")
for res_object in results_response["TestingApplications"]:
    current_object = res_object["PlatformName"]
    if(current_object == "Mobile devices"):
        f3.write("-----------------------------------------------------------------\n Current Results for " + res_object["ApplicationName"] + "\n The current state is: \n " + res_object["State"] + "-----------------------------------------------\n")
        f3.write(json.dumps(res_object))
        f3.write("-----------------------------------------------\n")
f3.close()
'''


