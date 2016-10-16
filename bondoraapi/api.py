import sys
import requests
import account
import json

#
# Docs:
# https://api.bondora.com/Intro
#

bondora_base_url = "https://api.bondora.com"
a = account.Account()
token = a.token


def translate_status_code_to_string(status_code):
    """
    Translate bid status code from integer to a human understandable string
    """
    known_status_codes = {0: "Pending",
                          1: "Open",
                          2: "Successful",
                          3: "Failed",
                          4: "Cancelled",
                          5: "Accepted"}
    if status_code in known_status_codes:
        return known_status_codes[status_code]
    else:
        return "Unknown code: {}".format(status_code)


def make_post_request(request_url, content):
    full_url = "{}/{}".format(bondora_base_url, request_url)
    headers = {"Authorization": "Bearer {}".format(token),
               "Content-Type": "application/json"}
    return requests.post(full_url, headers=headers, data=json.dumps(content))


def make_bid(auction_id, bid_size=5):
    url = "/api/v1/bid"
    # Create a bid JSON payload
    bid = '''
    {{
        "Bids":
            [
                {{
                    "AuctionId": "{auction_id}",
                    "Amount": {bid_size},
                    "MinAmount": 5.0
                }}
            ]
    }}

    '''

    bid = json.loads(bid.format(auction_id=auction_id,
                                bid_size=float(bid_size)))
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


def get_auction(auction_id):
    url = "/api/v1/auction/{auction_id}".format(auction_id=auction_id)
    return make_get_request(url)


def get_bids(count=10):
    """ Return a list of bids, sorted by bid date"""
    url = "/api/v1/bids"
    bids = make_get_request(url)
    # sort bids by 'BidRequestedDate'
    sorted_bids = sorted(bids, key=lambda item: item['BidRequestedDate'])
    return sorted_bids[-count:]


def get_investments(count=10):
    url = "/api/v1/account/investments"
    investments = make_get_request(url)
    sorted_investments = sorted(investments,
                                key=lambda item: item['PurchaseDate'])
    return sorted_investments[-count:]
