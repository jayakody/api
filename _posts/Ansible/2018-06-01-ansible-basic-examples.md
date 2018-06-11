---
date: 2018-06-01
title: Basic Examples
categories:
  - Ansible
description: "Basic Ansible Automation with Big Cloud Fabric"
type: Document
---

## Introduction

This example walk you through the basics of automation using Ansible in Big Cloud Fabric.

## Step 1: Login to the Fabric

Following code will initiate a connection to the Big Cloud Fabric. 

~~~ python

import requests
import json
import sys

requests.packages.urllib3.disable_warnings()

controller_ip = "10.10.10.1"
username = "admin"
password = "password"
cookie = ""

def controller_request(method, path, data=""):
    if not controller_ip:
        print 'You must set controller_ip to the IP address of your BCF controller'
    controller_url = "https://%s:8443" % controller_ip
    # append path to the controller url, e.g. "https://192.168.23.98:8443" + "/api/v1/auth/login"
    url = controller_url + path
    # if a cookie exists then use it in the header, otherwise create a header without a cookie
    if cookie:
        session_cookie = 'session_cookie=%s' % cookie
        headers = {"content-type": "application/json", 'Cookie': session_cookie}
    else:
        headers = {"content-type": "application/json"}
    # submit the request
    response = requests.request(method, url, data=data, headers=headers, verify=False)
    # if content exists then return it, otherwise return the HTTP status code
    if response.content:
        return json.loads(response.content)
    else:
        return response.status_code

~~~

## Step 2: Authenticating with the Big Cloud Fabric

Using the `response.status_code` returned by the previous step folloing function will authenticate with the Big Cloud Fabric

```python
def authentication():
    global cookie
    method = 'POST'
    path = "/api/v1/auth/login"
    data = '{"user":"%s", "password":"%s"}' % (username, password)
    json_content = controller_request(method, path, data)
    cookie = json_content['session_cookie']

def authentication_revoke():
    method = "DELETE"
    path = '/api/v1/data/controller/core/aaa/session[auth-token="%s"]' % cookie
    status_code = controller_request(method, path)

if __name__ == '__main__':
    authentication()
```

