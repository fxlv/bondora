#!/usr/bin/env python
from prettytable import PrettyTable
from bondoraapi import api

payload = api.get_auctions()

print "We have {} items to work with".format(len(payload))

t = PrettyTable()
t.field_names = ["Rating", "AppliedAmount", "UserName", "City", "IncomeTotal",
                 "RemainingAmount", "AuctionId"]

for item in payload:
    if item["Rating"] in ("AA", "A", "B", "C"):
        t.add_row([item["Rating"], item["AppliedAmount"], item["UserName"],
                   item["City"], item["IncomeTotal"], item[
                       "RemainingAmount"], item["AuctionId"]])

print t
