#!/usr/bin/python3
""""""
from pymongo.errors import PyMongoError
from models.engine.dbstorage import MongoDBClient
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG)

class File:
    """"""

    def __init__(self):
        """"""

        self._id = MongoDBClient()
        self.time = datetime.utcnow()

    def reg_folder(self, col, email, folderName):
        """"""
        try:
            user = self._id.find_one(col, {"folderName": folderName})
            if user:
                raise ValueError(f"{folderName} Folder already exists")
            data = {
                "email": email,
                "folderName": folderName,
                "time": self.time
                }
            return self._id.insert_one(col, data)
        except PyMongoError as e:
            print(f"Error registering user: {str(e)}")
            raise e

    def reg_file(self, col, email, folderName, file):
        """"""

        try:
            user = self._id.find_one(col, {"email": email, "folderName": folderName, "file.name": file['name']})
            if user:
                raise ValueError(f"{file['name']} file already exists in {folderName} Folder")
            data = {
                "email": email,
                "folderName": folderName,
                "file": file,
                "time": self.time
                } 
            return self._id.insert_one(col, data)
        except PyMongoError as e:
            print(f"Error registering user: {str(e)}")
            raise e

    def find_folder(self, col, email, folderName):
        """"""

        if folderName is None or email is None:
            return None

        try:
            user = self._id.find_one(col, {"email": email, "folderName": folderName})
            if not user:
                raise ValueError("{folderName} Folder not Found")
            return user
        except PyMongoError as e:
            print(f"Error registering user: {str(e)}")
            raise e

    """def find_file(self, col, email, folderName, file):
        """"""

        if folderName is None or file is None or email is None:
            return None

        try:
            user = self._id.find_one(col, email=email, folderName=folderName, file=file)
            if not user:
                raise ValueError("{file} File not Found")
            return user
        except PyMongoError as e:
            print(f"Error registering user: {str(e)}")
            raise e"""

    def find_time(self, col, time):
        """"""

        if time is None:
            return None

        try:
            user = self._id.find_many(col, {"time": time})
            if not user:
                raise ValueError("This {time} time not Found")
            return user
        except PyMongoError as e:
            print(f"Error registering user: {str(e)}")
            raise e

    def delete_folder(self, col, email, folderName):
        """"""

        if folderName is None or email is None:
            return None

        try:
            user = self._id.find_one(col, {"email": email, "folderName": folderName})
            if not user:
                raise ValueError(f"{folderName} folder not Found")
            self._id.delete_one(col, {"_id": user["_id"], "folderName": folderName})
            return {"message": f"Folder '{folderName}' deleted successfully"}
        except PyMongoError as e:
            print(f"Error registering user: {str(e)}")
            raise e

    def delete_file(self, col, email, folderName, file):
        """"""

        if file is None or email is None or folderName is None:
            return None

        try:
            user = self._id.find_one(col, {"email": email, "folderName": folderName, "file": file})
            name = file['name']
            if not user:
                raise ValueError(f"'{name}' file not Found")
            result = self._id.delete_one(col, {"_id": user["_id"], "file": file})
            if result > 0:
                return {"message": f"file '{file}' deleted successfully"}
            return None
        except PyMongoError as e:
            raise e


    def update_folder(self, col, folderName):
        """"""

        if folderName is None:
            return None
        try:
            user = self._id.find_one(col, {"folderName": folderName})
            if not user:
                raise ValueError(f"Coulf not {folderName} folder")
            result = self._id.update_one(col, {"_id": user["_id"], "folderName": folderName})
            if result > 0:
                return folderName
        except PyMongoError as e:
            print(f"Error registering user: {str(e)}")
            raise e

    def update_file(self, col, email, folderName, old_file, new_file):
        """"""

        if not old_file or not new_file:
            return None
        try:
            user = self._id.find_one(col, {"email": email, "folderName": folderName, "file.name": old_file})
            if not user:
                raise ValueError(f"Could not find file {old_file} in folder '{folderName}'")
            result = self._id.update_one(col, {"_id": user["_id"], "file.name": old_file}, {"file.name": file['name'], "file.content": file['content']})
            if result > 0:
                return new_file
            return None
        except PyMongoError as e:
            raise e

    def check_string(self, col, folderName, file):
        """"""

        dlist = []
        if folderName is None or file is None:
            return None
        try:
            files = self._id.find_many(col, {"folderName": folderName})

            for one in files:
                dlist.append(one['file']['content'])
            for content in dlist:
                end = 10
                for k in range(len(content) - end + 1):
                    substring = content[k:k + end]
                    if substring in file['content']:
                        last = self._id.find_many(col, {"folderName": folderName, "file.content": content})
                        return([substring, [doc["file"]["name"] for doc in last]])
            return None
        except PyMongoError as e:
            logging.error(f"Error updating file: {str(e)}")
            raise e
