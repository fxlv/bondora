"""
Import Bondora account settings

Look for the settings file in:
    - current directory
    - .bondora directory in user's home directory

"""
import os
import yaml


def load():
    config_file = "config.yaml"
    search_paths = [os.getcwd(), "{}/.bondora".format(os.environ["HOME"])]

    for path in search_paths:
        path = "{}/{}".format(path, config_file)
        if os.path.exists(path):
            with open(path) as config_file:
                config = yaml.load(config_file)
                if "token" in config:
                    return config
    return False


def get_token():
    return load()["token"]


def get_accepted_loan_ratings():
    conf = load()
    if "accepted_loan_ratings" in conf:
        return conf["accepted_loan_ratings"]
    else:
        return ["AA", "A"]


def get_accepted_countries():
    conf = load()
    if "accepted_countries" in conf:
        return conf["accepted_countries"]
    else:
        return []  # return empty list


def get_min_balance():
    conf = load()
    if "min_balance" in conf:
        return conf["min_balance"]
    else:
        return 5  # default
