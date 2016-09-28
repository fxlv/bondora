#!/usr/bin/env python
import os
import sys
import requests
import account
from prettytable import PrettyTable
import ipdb

#
# Docs:
# https://api.bondora.com/Intro
#


def get_auctions():
    bondora_base_url = "https://api.bondora.com"
    url = "{}/api/v1/auctions".format(bondora_base_url)

    token = account.get_token()

    headers = {"Authorization": "Bearer {}".format(token)}

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
    return payload
