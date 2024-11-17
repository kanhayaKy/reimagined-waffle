# Simple requests
from urllib import request, parse


## Get request
url = "http://httpbin.org/get"
params = {"foo": "bar"}

querystring = parse.urlencode(params)

u = request.urlopen(url + "?" + querystring)
response = u.read()
print(response)


# Post request
url = "http://httpbin.org/post"

params = {"foo": "bar"}
querystring = parse.urlencode(params)

u = request.urlopen(url, querystring.encode("ascii"))
response = u.read()
print(response)


# Request with custom headers

url = "http://httpbin.org/post"

headers = {"spam": "eggs"}
params = {"foo": "bar"}

querystring = parse.urlencode(params)

req = request.Request(url, querystring.encode("ascii"), headers=headers)

u = request.urlopen(req)
response = u.read()
print(response)


# Advance usage using requests library
import requests

url = "http://httpbin.org/post"

headers = {"spam": "eggs"}
params = {"foo": "bar"}

response = request.post(url, data=params, headers=headers)

print(response.text)


## Extract header data

import requests

resp = requests.head("http://www.python.org/index.html")

status = resp.status_code
last_modified = resp.headers["last-modified"]
content_type = resp.headers["content-type"]
content_length = resp.headers["content-length"]

print(last_modified, content_type, content_length)


## Making auth request

import requests

resp = requests.get(
    "http://pypi.python.org/pypi?:action=login", auth=("user", "password")
)


## File uploading

import requests

files = {"file": ("data.csv", open("data.csv", "rb"))}

response = requests.post(url, files=files)
