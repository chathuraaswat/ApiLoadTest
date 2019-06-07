import csv
import logging, sys
import hmac
import string
import hashlib
import base64
import json

from globe import config 
from modules.admin import auth

from locust import HttpLocust, TaskSet, task 
from locust.stats import RequestStats

global json_data
global accress_token
global path


class runrunnerAdmin(TaskSet):
 
    

    @task
    def on_start(self):
        
        #Object from globle file 
        conf = config.config()
        path = conf.getLocation()
       
        with open('/Users/chathuraworkaux/Desktop/ziwoLoadTestv0.1/globe/credentials.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                #print(" Login --->"+row[0]+" Who has Password --->"+row[1])
                secret = row[1]
                message = row[0]+row[1]
                key = secret.encode('utf-8')
                hmac_result = hmac.new(key, message.encode('utf-8'), hashlib.sha256)
                EncriptedPW = base64.b64encode(hmac_result.digest())

                #object from Admin Auth
                login = auth.auth()

                #login Service Auth 
                print("Login User "+row[0])
                response=login.login(row[0],EncriptedPW)
                assert response.status_code is 200, "Unexpected response code: " + response.status_code
                json_data =json.loads(response.text)
                accress_token =json_data['content']["access_token"] 
                #get Login User details 
                print("Get Details for logged User "+row[0])
                response=login.getLogUser(accress_token)
                assert response.status_code is 200, "Unexpected response code: " + response.status_code
            
class LoginWithUniqueUsersTest(HttpLocust):
    task_set = runrunnerAdmin
