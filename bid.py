#!/usr/bin/env python
import sys
import json
from bondoraapi import api
from prettytable import PrettyTable

if not len(sys.argv) == 2:
    print "provide AuctionId as the first and only argument"
    sys.exit(1)

auction_id = sys.argv[1]

bid_result = api.make_bid(auction_id)
if not bid_result:
    print "Bid failed"

print "Bid successfull"
# result is a list, we only care about the first element
bid_result = bid_result[0]

t = PrettyTable()

t.field_names = ["AuctionId", "Amount", "MinAmount"]
t.add_row([bid_result["AuctionId"], bid_result["Amount"], bid_result[
    "MinAmount"]])
print t
