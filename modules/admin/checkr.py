from locust import HttpLocust, TaskSet, task 
from locust import clients
from locust.clients import HttpSession 


from locust import HttpLocust, TaskSet, task, events
from bs4 import BeautifulSoup
import random

def is_static_file(f):
    if "https://qa.aswat.co" in f:
        return True
    else:
        return False

def fetch_static_assets(session, response):
    resource_urls = set()
    soup = BeautifulSoup(response.text, "html.parser")

    for res in soup.find_all(src=True):
        url = res['src']
        if is_static_file(url):
            resource_urls.add(url)
        else:
            print "Skipping: " + url

    for url in set(resource_urls):
        #Note: If you are going to tag different static file paths differently,
        #this is where I would normally do that.
        session.client.get(url, name="(Static File)")

class AnonBrowsingUser(TaskSet):
    @task(10)
    def frontpage(self,l):
        response = l.client.get("/")
        fetch_static_assets(l, response)

class AuthBrowsingUser(TaskSet):
    def on_start(self,l):
        response = l.client.get("/user/login", name="Login")
        soup = BeautifulSoup(response.text, "html.parser")
        drupal_form_id = soup.select('input[name="form_build_id"]')[0]["value"]
        r = l.client.post("/user/login", {"name":"nnewton", "pass":"hunter2", "form_id":"user_login_form", "op":"Log+in", "form_build_id":drupal_form_id})

    @task(10)
    def frontpage(self,l):
        response = l.client.get("/", name="Frontpage (Auth)")
        fetch_static_assets(l, response)

class WebsiteAuthUser(HttpLocust):
    task_set = AuthBrowsingUser    

class WebsiteAnonUser(HttpLocust):
    task_set = AnonBrowsingUser