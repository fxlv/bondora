#!/usr/bin/env python
import os
import sys
import requests
import account
import json

#
# Docs:
# https://api.bondora.com/Intro
#
if not len(sys.argv) == 2:
    print "provide AuctionId as the first and only argument"
    sys.exit(1)

auction_id = sys.argv[1]
bid = '''
{{
    "Bids": 
        [ 
            {{
                "AuctionId": "{auction_id}", 
                "Amount": 5.0, 
                "MinAmount": 5.0 
            }}
        ]
}}

'''

bid = json.loads(bid.format(auction_id=auction_id))

url = "https://api.bondora.com/api/v1/bid"

token = account.get_token()

headers ={"Authorization":"Bearer {}".format(token), "Content-Type":"application/json"}
response = requests.post(url, headers=headers, data=json.dumps(bid))

print response


print response.json()
