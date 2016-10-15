# Bondora

[![Build Status](https://travis-ci.org/fxlv/bondora.svg?branch=master)](https://travis-ci.org/fxlv/bondora)
---

For whatever reason Bondora really seems to be limiting what is possible via the web page.
Some investments never even show up on the web page.

API allows you to have better investment opportunities (or so it seems).

I use these scripts to invest a bit
They aren't neccesarelly well written or anything, but they do get the job done.

# This is unofficial 
Just to clarify, I'm in no way related to Bondora. 
My only aim is to make investig a bit more flexible.
As long as they don't change the API, this should work.


# Installing
Clone this repo and install the dependencies with
```
pip install -r requirements.txt
```

Afterwards you need to create the configuration file - `config.yaml`.
It can be located either in the current directory or in `~/.bondora/`.
I'd recommend going with `~/.bondora/config.yaml`.

Example configuration file is provided in the `examlpes` directory.
For starters, you only need to generate a token and put it in the config file.
Look at the example for more details.

## Older python
If your python version is < 2.7.9, you'll have to install the following packages to avoid SSL Warnings:
```
pip install pyopenssl ndg-httpsclient pyasn1
```

# Using
The main script `bondora.py` takes several arguments.
Run it without any to get help on usage.

## Show auctions

`./bondora.py -a` will produce something like this (example output, not real data):

```
There are currently 4 auctions available
2 auctions match your criteria
+--------+-----------+---------------+-------------+-----------------+---------------+-----------+--------------------------------------+
| Rating |  UserName | AppliedAmount | IncomeTotal | RemainingAmount |      City     | BidExists |              AuctionId               |
+--------+-----------+---------------+-------------+-----------------+---------------+-----------+--------------------------------------+
|   A    | BO0001111 |    10000.0    |    1234.0   |     -1234.0     |    TALLINN    |    True   | 12345678-llll-laks-12qw-73737373hhhh |
|   C    | BO0001112 |    12341.0    |    5432.0   |      1234.0     |    HELSINKI   |   False   | 12345678-kkkk-ytre-34er-99ajjsh777aa |
+--------+-----------+---------------+-------------+-----------------+---------------+-----------+--------------------------------------+`
```

## Make a bid 
```
./bondora.py -b <AuctionId>
```
Example:
```
./bondora.py -b 12345678-llll-laks-12qw-73737373hhhh
```

## Get a list of bids you've made
```
./bondora.py --bids
```
Example:
```
+--------------------------------------+-----------------+--------------------+------------+-------------------------+---------------------------+---------------------------+
|              AuctionId               | ActualBidAmount | RequestedBidAmount | StatusCode | IsRequestBeingProcessed |      BidRequestedDate     |      BidProcessedDate     |
+--------------------------------------+-----------------+--------------------+------------+-------------------------+---------------------------+---------------------------+
| 12345678-llll-laks-12qw-73737373hhhh |       10.0      |        10.0        | Successful |          False          | 2016-09-10T12:00:00+00:00 | 2016-09-10T12:00:00+00:00 |
+--------------------------------------+-----------------+--------------------+------------+-------------------------+---------------------------+---------------------------+
```

## Balance
You can check on your balance with:
```
./bondora.py --balance
```

## Auto invest
Automatically bid in available auctions if certain criteria are met.
Namely, risk rating, country and income verification.

Add it to cron and forget about manual actions.

Run:
```
./bondora.py --auto
```
