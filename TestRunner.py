
import csv
import logging, sys
import hmac
import string
import hashlib
import base64
import json

from globe import config 
from modules.admin import auth
from modules.agent import authAgent
from locust import HttpLocust, TaskSet, task 
from locust.stats import RequestStats
from globe import util


class runnerAgent(TaskSet):
 
    
    global json_data
    global accress_token
    global path
    global ccLogin
    global API_KEY

    @task
    def Login(self):
        
        #Object from globle file 
        conf = config.config()
        path = conf.getLocation()
        #object from Admin Auth
        login = authAgent.authAgent()
        PWConbv = util.util()
       
        with open('/home/aux-120/LoadTestScripts/ziwoLoadTestv0.1/globe/credentials.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                print(" Login Agent with Username--->"+row[0]+" Who has Password --->"+row[1])
                EncriptedPW=PWConbv.hashconversion(row[0],row[1])
                #login Service Auth 
                Loginresponse=login.login(row[0],EncriptedPW)
                assert Loginresponse.status_code is 200, "Unexpected response code: " + Loginresponse.status_code
                json_data =json.loads(Loginresponse.text)
                accress_token =json_data['content']["access_token"] 
                ccLogin =json_data ['content']["ccLogin"]
                API_KEY = conf.getAPI_key()
                if Loginresponse.status_code==200:
                    login.loginposition(API_KEY,ccLogin)
                else:
                    login.login(row[0],EncriptedPW)
                #positionLogout=login.Logout(accress_token)



class LoginWithUniqueUsersTest(HttpLocust):
    task_set = runnerAgent
