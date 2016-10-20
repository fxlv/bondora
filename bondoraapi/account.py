"""Bondora account settings.

Look for the settings file in:
    - current directory
    - .bondora directory in user's home directory

"""
import os
import yaml
import logging


class Account(object):
    """
    Bondora account settings.

    Finds and reads the config file and stores the configuration
    settings as object attributes.
    """

    def __init__(self):
        """Initialize account.

        If some of the optional settings are not defined
        fall back to using defaults.
        """
        logging.debug("Account object is being created")
        self.config = None
        self.config_path = None
        self.load()
        self.token = self.config['token']
        # initialize with defaults if needed
        if "accepted_loan_ratings" in self.config:
            self.accepted_loan_ratings = self.config["accepted_loan_ratings"]
        else:
            self.accepted_loan_ratings = ["AA", "A"]
        if "accepted_countries" in self.config:
            self.accepted_countries = self.config["accepted_countries"]
        else:
            self.accepted_countries = ["EE"]
        if "min_balance" in self.config:
            self.min_balance = self.config["min_balance"]
        else:
            self.min_balance = 5
        if "max_bid" in self.config:
            self.max_bid = self.config["max_bid"]
        else:
            self.max_bid = 5
        if "min_bid" in self.config:
            self.min_bid = self.config["min_bid"]
        else:
            self.min_bid = 5

    def load(self):
        """Find and load the configuration file."""
        config_file = "config.yaml"
        if "HOME" in os.environ:
            search_paths = [os.getcwd(), "{}/.bondora".format(os.environ["HOME"])]
        else:
            logging.debug("You don't appear to have 'HOME' environment variable set.'")
            search_paths = [os.getcwd()]
        logging.debug("Search paths: %s", search_paths)

        for path in search_paths:
            file_path = "{}/{}".format(path, config_file)
            if os.path.exists(file_path):
                with open(file_path) as config_file:
                    self.config = yaml.load(config_file)
                    self.config_path = path
                    if "token" not in self.config:
                        msg = "Account Token missing. Check your configuration!"
                        raise KeyError(msg)
                    else:
                        logging.debug("Config loaded successfully")
