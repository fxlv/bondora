#!/usr/bin/env python
#
# Script for working with Bondora (bondora.com) API
# Currently supported features:
#   - retrieve auctions
#   - make bids
#   - get account balance
#
# Safety not guaranteed
# Kaspars Mickevics <kaspars@fx.lv>
#
import argparse
from prettytable import PrettyTable
from bondoraapi import account, api


def parse_args():
    parser = argparse.ArgumentParser(description="BondoraPy")
    parser.add_argument('-a', action='store_true', help='Show auctions')
    parser.add_argument('-b', action='store_true', help='Make a bid')
    parser.add_argument('--balance', action='store_true', help='Show balance')
    return parser, parser.parse_args()


def main():
    parser, args = parse_args()
    if args.a:
        show_auctions()
    elif args.b:
        print "Make a bid"
    elif args.balance:
        print "Show balance"
    else:
        parser.print_help()


def show_auctions():
    accepted_loan_ratings = account.get_accepted_loan_ratings()
    payload = api.get_auctions()

    print "There are currently {} auctions available".format(len(payload))
    # now filter out the auctions that do not match our risk rating criteria
    auctions = []
    my_bids = api.get_bids()
    for item in payload:
        if item["Rating"] in accepted_loan_ratings:
            # cross check each auction against my bids
            item["BidExists"] = False # assume bid does not exists by default
            for bid in my_bids:
                if item["AuctionId"] == bid["AuctionId"]:
                    item["BidExists"] = True
            auctions.append(item)
    print "{} auctions match our criteria".format(len(auctions))
    print_table(
        ["Rating", "UserName", "AppliedAmount", "IncomeTotal",
         "RemainingAmount", "City", "BidExists", "AuctionId"], auctions)


def print_table(header, rows):
    """Print a pretty table from a set of keys and data"""
    table = PrettyTable()
    table.field_names = header
    for row in rows:
        row_content = []
        for key in header:
            row_content.append(row[key])
        table.add_row(row_content)
    print table


def make_bid():
    pass


def show_balance():
    pass


if __name__ == "__main__":
    main()
