#!/usr/bin/env python
import os
import sys
import requests
import account

#
# Docs:
# https://api.bondora.com/Intro
#

url = "https://api.bondora.com/api/v1/account/balance"

token = account.get_token()

headers ={ "Authorization":"Bearer {}".format(token)} 

response = requests.get(url, headers=headers)

if not response.ok:
    print "Bad response"
    print response.json()
    sys.exit(1)
response_json = response.json()

if not response_json['Success']:
    print "We have response, but it's not a success"
    sys.exit(1)

payload = response_json['Payload']


print response_json
