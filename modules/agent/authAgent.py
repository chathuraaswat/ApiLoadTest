

from locust import HttpLocust, TaskSet, task 
from locust import clients
from locust.clients import HttpSession 
import requests
global BaseUrl 
class authAgent():
    # conf = config.config()
    BaseUrl = "https://qa-api.aswat.co"
    #Auth API's Definitions
    def login( self,userName,passWord):
        s = HttpSession("https://qa-api.aswat.co")
        response = s.post("https://qa-api.aswat.co/auth/login", {"username":userName, "password":passWord})
        return response
    def loginposition( self,api_key,cclogin,):
        s = HttpSession("https://qa-api.aswat.co")
        request="https://qa-api.aswat.co/integrations/cti/agents/"+cclogin+"/login/agent-"+cclogin
        print(request)
        response = s.post(request, headers = {"api_key":api_key, "Content-Type":"application/json"})
        return response
    def Logout( self,access_token):
        s = HttpSession("https://qa-api.aswat.co")
        response = s.post("https://qa-api.aswat.co/auth/logout", headers = {"api_key":access_token})
        return response

						