#!/usr/bin/env python
from prettytable import PrettyTable
from bondoraapi import api


def bidstatus(status_code):
    known_status_codes = {0: "Pending",
                          1: "Open",
                          2: "Successful",
                          3: "Failed",
                          4: "Cancelled",
                          5: "Accepted"}
    if status_code in known_status_codes:
        return known_status_codes[status_code]
    else:
        return "Unknown"


response = api.get_bids()
import ipdb
ipdb.set_trace()

t = PrettyTable()
t.field_names = ["AuctionId", "ActualBidAmount", "RequestedBidAmount",
                 "StatusCode", "IsRequestBeingProcessed", "BidRequestedDate",
                 "BidProcessedDate"]

for line in response:
    t.add_row([line["AuctionId"], line["ActualBidAmount"], line[
        "RequestedBidAmount"], bidstatus(line["StatusCode"]), line[
            "IsRequestBeingProcessed"], line["BidRequestedDate"], line[
                "BidProcessedDate"]])

print t
