#!/usr/bin/env python
#
# Script for working with Bondora (bondora.com) API
# Currently supported features:
#   - retrieve auctions
#   - make bids
#   - get account balance
#   - auto invest
#
# Safety not guaranteed
# Kaspars Mickevics <kaspars@fx.lv>
#
import sys
import argparse
from prettytable import PrettyTable
import storage
import logging
import time
import random
import datetime

# logging must be initialized before anything else
logging.basicConfig(filename="bondora.log",
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

import bondoraapi.api
import bondoraapi.account

# initialize Bondora account
A = bondoraapi.account.Account()
S = storage.Storage(A)
API = bondoraapi.api.Api(S)

max_runs_per_hour = 15


def parse_args():
    """Handle the command line arguments."""
    parser = argparse.ArgumentParser(description="BondoraPy")
    parser.add_argument('-a', action='store_true', help='Show auctions')
    parser.add_argument('-b', metavar="AuctionId", help='Make a bid')
    parser.add_argument('--auto', action='store_true', help='Auto invest mode')
    parser.add_argument('--sched', action='store_true', help='Scheduler mode')
    parser.add_argument('--bids', action='store_true', help='Show your bids')
    parser.add_argument('--balance', action='store_true', help='Show balance')
    parser.add_argument('--investments',
                        action='store_true',
                        help='Show investments')
    return parser, parser.parse_args()


def main():
    """Call appropriate function based on CLI arguments."""
    parser, args = parse_args()
    if args.a:
        show_auctions()
    elif args.b:
        make_bid(args.b)
    elif args.auto:
        auto()
    elif args.sched:
        scheduler()
    elif args.balance:
        show_balance()
    elif args.bids:
        show_bids()
    elif args.investments:
        show_investments()
    else:
        parser.print_help()


def auction_exists(auction_id):
    """Return True if such auction exists."""
    for auction in API.get_auctions():
        if auction["AuctionId"] == auction_id:
            return True
    return False


def show_auctions():
    """Print a table of current auctions that match configured criteria."""
    payload = API.get_auctions()

    print "There are currently {} auctions available".format(len(payload))
    # now filter out the auctions that do not match our risk rating criteria
    auctions = []
    my_bids = API.get_bids()
    for item in payload:
        if item["Rating"] in A.accepted_loan_ratings:
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
    """Print a pretty table from a set of keys and data."""
    table = PrettyTable()
    table.field_names = header
    if type(rows) is not list:
        rows = [rows]  # there can also be a single row
    for row in rows:
        row_content = []
        for key in header:
            # some things can be made more human friendly
            if key == "StatusCode":
                cell_value = API.translate_status_code_to_string(row[key])
            else:
                cell_value = (row[key])
            # add cell value to cell
            row_content.append(cell_value)

        table.add_row(row_content)
    print table


def make_bid(auction_id):
    """Submit a bid to API."""
    if auction_exists(auction_id):
        API.make_bid(auction_id)
    else:
        print "Such auction does not seem to exist"
        print "AuctionId: {}".format(auction_id)
        sys.exit(1)


def show_balance():
    """Print a table that shows account balance."""
    logging.debug("Show balance")
    print_table(
        ["Balance", "Reserved", "BidRequestAmount",
         "TotalAvailable"], API.get_balance())


def show_bids():
    """Print a table of current bids."""
    logging.debug("Show bids")
    keys = ["AuctionId", "ActualBidAmount", "RequestedBidAmount", "StatusCode",
            "IsRequestBeingProcessed", "BidRequestedDate", "BidProcessedDate"]
    print_table(keys, API.get_bids())


def show_investments():
    """Print a table of current investments."""
    logging.debug("Show investments")
    investments = API.get_investments()
    keys = ["Rating", "UserName", "Country", "PurchasePrice",
            "PrincipalRepaid", "Interest", "PurchaseDate"]
    print_table(keys, investments)


def scheduler():
    """Scheduler mode.

    Glorified 'while True' loop basically.
    Try to be more active between 08:00 and 17:00.
    Max 10 runs per hour.
    """
    while True:
        date = datetime.datetime.now()
        hour = date.hour
        # working hours, between 08:00 and 18:00
        if hour > 7 and hour < 18:
            # sleep time: random period between 1 - 6 minutes
            sleep_time = random.randrange(60, 360)
        else:
            # sleep time: random period between 30 - 60 minutes
            sleep_time = random.randrange(1800, 3600)
        logging.debug("This hour: %s", S.this_hour)

        if S.last_sched_run.hour != hour:
            logging.debug("New hour. Resetting hourly run counter.")
            S.save("this_hour", 0)
        else:
            # this is not the first time we run this hour,
            # check that max_runs_per hour is not reached
            if int(S.this_hour) < max_runs_per_hour:
                auto()
                logging.debug("Incrementing hourly run counter.")
                S.save("this_hour", S.this_hour + 1)
            else:
                logging.debug("Max runs per hour reached")
        S.save("last_sched_run", date)

        logging.debug("Sleeping for %s seconds", sleep_time)
        time.sleep(sleep_time)


def auto():
    """Auto invest mode.

    Go into a loop of:
    - Retrieve auctions
    - Check each auction:
        * Have I already invested in it
        * Is the risk rating acceptable
        * Is income verified
        * Is it already fully funded?
        * do I have enough funds to make a bid
    - if criteria match, make a bid
        * bid size depends on risk rating
    """
    logging.debug("Running auto invest")
    # gather all the information needed first
    my_balance = API.get_balance()
    my_bids = API.get_bids()
    available_auctions = API.get_auctions()

    # must have at least 1 auctions to continue
    if len(available_auctions) < 1:
        print "No auctions available at this time."
        return False
    # now iterate over the available auctions
    # and check for criteria match

    for auction in available_auctions:
        print "Auction: {}, ".format(auction["AuctionId"]),
        # First of all, do I have enough balance to invest?
        print "Available balance?",
        if not my_balance["TotalAvailable"] >= A.min_balance:
            print "No. Skip."
            continue
        else:
            print "Yes.",

        # have I already invested in it?
        have_i_already_invested = False
        print "Already invested in it?",
        for bid in my_bids:
            if auction["AuctionId"] == bid["AuctionId"]:
                # I have already invested, skip it
                have_i_already_invested = True
                break

        if have_i_already_invested:
            print "Yes. Skipping."
            continue
        else:
            print "No.",

        # lets check if it's still available for investing
        # and has not been fully funded
        print "Fully funded? ",
        if auction["RemainingAmount"] < 0:
            print "Yes. Skipping."
            continue
        else:
            print "No.",

        # now, let's check if the country is in my list
        print "Accepted country? ",
        if not auction["Country"] in A.accepted_countries:
            print "No. Skiping."
            continue
        else:
            print "Yes",

        # is the risk rating acceptable?
        print "Acceptable risk rating? ",
        if not auction["Rating"] in A.accepted_loan_ratings:
            print "No. Skipping."
            continue
        else:
            print "Yes.",

        # at this point we can set the bid size
        if auction["Rating"] in ["AA", "A"]:
            bid_size = A.max_bid
        else:
            bid_size = A.min_bid
        print "Bid size: {} eur,".format(bid_size),
        # income verified?
        # integer must be above 1
        # 1 == not verified, 2 - 4 different types of verified ones
        print "Income verified? "
        if not auction["VerificationType"] < 2:
            print "No. Skip."
            continue
        else:
            print "Yes.",

        # Invest!
        print "I shall invest in {} now!".format(auction["AuctionId"])
        API.make_bid(auction["AuctionId"], bid_size)
        # decrement available balance to avoid querying api
        my_balance["TotalAvailable"] -= 5

        # rinse and repeat


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Ctrl+c pressed. Exiting.")
        print "Exiting..."
        sys.exit(0)
