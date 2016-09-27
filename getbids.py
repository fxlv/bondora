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
def bidstatus(status_code):
    known_status_codes = {0:"Pending", 1:"Open", 2:"Successful", 3:"Failed", 4:"Cancelled", 5:"Accepted"}
    if status_code in known_status_codes:
        return known_status_codes[status_code] 
    else:
        return "Unknown"

url = "https://api.bondora.com/api/v1/bids"

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

t = PrettyTable()
t.field_names = ["AuctionId", "ActualBidAmount", "RequestedBidAmount", "StatusCode", "IsRequestBeingProcessed", "BidRequestedDate","BidProcessedDate"]
payload = response_json['Payload']
for line in payload:
    t.add_row([line["AuctionId"],line["ActualBidAmount"],line["RequestedBidAmount"],bidstatus(line["StatusCode"]),line["IsRequestBeingProcessed"],line["BidRequestedDate"],line["BidProcessedDate"]])

print t
