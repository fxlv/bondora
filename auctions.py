#!/usr/bin/env python
import os
import sys
import requests
import account
from prettytable import PrettyTable

#
# Docs:
# https://api.bondora.com/Intro
#

url = "https://api.bondora.com/api/v1/auctions"

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

print "We have {} items to work with".format(len(payload))

t = PrettyTable()
t.field_names = ["Rating","AppliedAmount","UserName","City","IncomeTotal","RemainingAmount","AuctionId"]

for item in payload:
    if item["Rating"] in ("AA", "A", "B", "C"):
        t.add_row([item["Rating"], item["AppliedAmount"], item["UserName"], item["City"], item["IncomeTotal"], item["RemainingAmount"], item["AuctionId"]])

print t


