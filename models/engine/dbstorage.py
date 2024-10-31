#!/usr/bin/python3
""""""
from pymongo import errors
import logging
from pymongo import MongoClient
from os import getenv


class MongoDBClient:
    """"""

    conn = {}

    def __init__(self):
        """"""

        libconnecthost = getenv("libconnecthost", "127.0.0.1")
        libconnectport = int(getenv("libconnectport", 27017))
        libConnectdb = getenv("libconnect", "libConnectdb")
        
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(f"Connecting to MongoDB at {libconnecthost}:{libconnectport}")

        try:
            self.connect = MongoClient(libconnecthost, libconnectport, serverSelectionTimeoutMS=5000)
            self.connect.server_info()  # Forces a call to the server to check if it's running
            self.db = self.connect[libConnectdb]
            self.db.command("ping")
            logging.debug(f"Successfully connected to MongoDB {libConnectdb}")
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise

    def createCollection(self, data):
        """"""

        try:
            if data not in self.db.list_collection_names():
                self.db.create_collection(data)
                print(f"Collection '{data}' created.")
            else:
                print(f"Collection '{data}' already exists.")
            return self.db[data]
        except errors.CollectionInvalid as e:
            print(f"Failed to create collection: {e}")

    def database_name(self, data):
        """"""

        self.datacollection = self.db.data
        return self.datacollection

    def insert_one(self, col, data):
        """"""

        result = col.insert_one(data)
        return col.find_one({"_id": result.inserted_id})

    def insert_many(self, col, data):
        """"""

        result = col.insert_many(data)
        return result.inserted_ids

    def find_one(self, col, query):
        """"""

        try:
            document = col.find_one(query)
            return document
        except Exception as e:
            raise e

    def find_many(self, col, query):
        """"""

        try:
            document = col.find(query)
            return list(document)
        except Exception as e:
            raise e

    def update_one(self, col, query, data):
        """"""

        result = col.update_one(query, {"$set": data})
        return result.modified_count

    def delete_one(self, col, query):
        """"""

        result = col.delete_one(query)
        return result.deleted_count

    def delete_many(self, col, query):
        """"""

        result = col.delete_many(query)
        return result.deleted_count
