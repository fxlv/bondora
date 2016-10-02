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
import sys
import argparse
from prettytable import PrettyTable
from bondoraapi import account, api


def parse_args():
    parser = argparse.ArgumentParser(description="BondoraPy")
    parser.add_argument('-a', action='store_true', help='Show auctions')
    parser.add_argument('-b', metavar="AuctionId", help='Make a bid')
    parser.add_argument('--bids', action='store_true', help='Show your bids')
    parser.add_argument('--balance', action='store_true', help='Show balance')
    parser.add_argument('--investments',
                        action='store_true',
                        help='Show investments')
    return parser, parser.parse_args()


def main():
    parser, args = parse_args()
    if args.a:
        show_auctions()
    elif args.b:
        make_bid(args.b)
    elif args.balance:
        show_balance()
    elif args.bids:
        show_bids()
    elif args.investments:
        show_investments()
    else:
        parser.print_help()


def auction_exists(auction_id):
    """Return True if such auction exists"""
    for auction in api.get_auctions():
        if auction["AuctionId"] == auction_id:
            return True
    return False


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
            item["BidExists"] = False  # assume bid does not exists by default
            for bid in my_bids:
                if item["AuctionId"] == bid["AuctionId"]:
                    item["BidExists"] = True
            auctions.append(item)
    print "{} auctions match your criteria".format(len(auctions))
    print_table(
        ["Rating", "UserName", "AppliedAmount", "IncomeTotal",
         "RemainingAmount", "City", "BidExists", "AuctionId"], auctions)


def print_table(header, rows):
    """Print a pretty table from a set of keys and data"""
    table = PrettyTable()
    table.field_names = header
    if type(rows) is not list:
        rows = [rows]  # there can also be a single row
    for row in rows:
        row_content = []
        for key in header:
            # some things can be made more human friendly
            if key == "StatusCode":
                cell_value = api.translate_status_code_to_string(row[key])
            else:
                cell_value = (row[key])
            # add cell value to cell
            row_content.append(cell_value)

        table.add_row(row_content)
    print table


def make_bid(auction_id):
    if auction_exists(auction_id):
        api.make_bid(auction_id)
    else:
        print "Such auction does not seem to exist"
        print "AuctionId: {}".format(auction_id)
        sys.exit(1)


def show_balance():
    print_table(
        ["Balance", "Reserved", "BidRequestAmount",
         "TotalAvailable"], api.get_balance())


def show_bids():
    keys = ["AuctionId", "ActualBidAmount", "RequestedBidAmount", "StatusCode",
            "IsRequestBeingProcessed", "BidRequestedDate", "BidProcessedDate"]
    print_table(keys, api.get_bids())


def show_investments():
    investments = api.get_investments()
    keys = ["Rating", "UserName", "Country", "PurchasePrice",
            "PrincipalRepaid", "Interest"]
    print_table(keys, investments)


if __name__ == "__main__":
    main()
