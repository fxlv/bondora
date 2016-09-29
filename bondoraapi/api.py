import sys
import requests
import account
import json
import ipdb

#
# Docs:
# https://api.bondora.com/Intro
#

bondora_base_url = "https://api.bondora.com"
token = account.get_token()

def make_post_request(request_url, content):
    full_url = "{}/{}".format(bondora_base_url, request_url)
    headers ={"Authorization":"Bearer {}".format(token), "Content-Type":"application/json"}
    return requests.post(full_url, headers=headers, data=json.dumps(content))


def make_bid(auction_id):
    url = "/api/v1/bid"
    # Create a bid JSON payload
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
    response = make_post_request(url, bid)
    if response.status_code == 202:
        response_json = response.json()
        if response_json["Success"]:
            return response_json["Payload"]
        else:
            print "Request was not successfull"
            print response_json
    else:
        print "Unexpected status code {}".format(response.status_code)
    return False


def make_get_request(request_url):
    full_url = "{}/{}".format(bondora_base_url, request_url)
    headers = {"Authorization": "Bearer {}".format(token)}

    response = requests.get(full_url, headers=headers)

    # Handle bad responses. Sort of. 
    if not response.ok:
        print "Bad response"
        print response.json()
        sys.exit(1)

    # At this point we have OK response
    response_json = response.json()

    if not response_json['Success']:
        print "We have response, but it's not a success"
        sys.exit(1)

    return response_json['Payload']



def get_balance():
    url = "/api/v1/account/balance"
    return make_get_request(url)


def get_auctions():
    url = "/api/v1/auctions"
    return make_get_request(url)


def get_bids():
    url = "/api/v1/bids"
    return make_get_request(url)


