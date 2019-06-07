

from locust import HttpLocust, TaskSet, task 
from locust import clients
from locust.clients import HttpSession 
import requests
global BaseUrl 
class auth():
    # conf = config.config()
    BaseUrl = "https://qa-api.aswat.co"
    #Auth API's Definitions
    def login( self,userName,passWord):
        s = HttpSession("https://qa-api.aswat.co")
        response = s.post("https://qa-api.aswat.co/auth/login", {"username":userName, "password":passWord})
        return response

    def getLogUser( self,accress_token):
        s = HttpSession("https://qa-api.aswat.co")
        response = s.get("https://qa-api.aswat.co/profile", headers={'access_token':accress_token})
        return response

