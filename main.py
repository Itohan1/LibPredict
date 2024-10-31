#!/usr/bin/python3
""""""
from models.engine.dbstorage import MongoDBClient

if __name__ == "__main__":
    data = {"username": "ItohanMomodu", "email": "blizzy@gmail.com"}

    col = MongoDBClient().createCollection("First_table")
    inserted_id = MongoDBClient().insert_one(col, data)
    print('my inserted data: {inserted_data}')

    query = {"username": "ItohanMomodu"}
    find_one = MongoDBClient().find_one(col, query)
    print(f"found document: {find_one}")

