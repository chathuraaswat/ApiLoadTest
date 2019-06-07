import hmac
import string
import hashlib
import base64
import json
from locust import HttpLocust, TaskSet, task
from locust import clients
from locust.clients import HttpSession
from bs4 import BeautifulSoup

from globe import config

global path
global session


conf= config.config()
path = conf.getAPI()

class util():
        
    def LoadResources(self,URL):
        session = HttpSession(path)
        response = session.get(path)
        resource_urls = set()
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup)
        for response in soup.find_all(src=True):
            url = response['src']
            resource_urls.add(URL)
            print ("Reading src-- > : " + url)


    # Auth API's Definitions
    def login(self, userName, passWord):
        session = HttpSession("https://qa-api.aswat.co")
        response = session.post(
            "https://qa-api.aswat.co/auth/login", {"username": userName, "password": passWord})
        return response

    def hashconversion(self,UserName,Password):
        secret = Password
        message = UserName+Password
        key = secret.encode('utf-8')
        hmac_result = hmac.new(key, message.encode('utf-8'), hashlib.sha256)
        EncriptedPW = base64.b64encode(hmac_result.digest())
        return EncriptedPW 