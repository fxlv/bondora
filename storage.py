"""Storage object for Bondora client.

Store various operational data, like:
- last success
- last failure
- last successfull bid
etc.
"""
import pickle
import os
import datetime
import logging


class Storage(object):
    """ Store operational data."""

    def __init__(self, A):
        """Set up the storage dictionary.

        Open it if file exists.
        If it does not, create an empty dictionary.
        """
        self.path = "{}/storage.p".format(A.config_path)
        logging.debug("Loading storage file")
        if os.path.exists(self.path):
            with open(self.path, "rb") as storage_file:
                self.storage = pickle.load(storage_file)
                logging.debug("Storage file loaded")
                logging.debug("Last save was: {}".format(self.storage[
                    "last_save"]))
        else:
            logging.debug(
                "storage file does not exist yet. Returning empty dict")
            self.storage = {}

    def __getattr__(self, key):
        """Lookup and return storage key:values."""
        logging.debug("Key '{}' requested from Storage".format(key))
        if key in self.storage:
            return self.storage[key]
        else:
            return None

    def save(self, key, value):
        """Save a key:value to storage."""
        logging.debug("Setting key '{}' = '{}'".format(key, value))
        self.storage[key] = value

    def __del__(self):
        """Save storage dictionary.

        Dump the storage dictionary to the pickle file
        file upon destruction of the object.
        """
        logging.debug("Storage cleanup in progress")
        self.storage["last_save"] = datetime.datetime.now()
        with open(self.path, "wb") as storage_file:
            pickle.dump(self.storage, storage_file)
        logging.debug("Cleanup complete")
