#!/usr/bin/python3
""""""
from pymongo.errors import PyMongoError
import uuid
import bcrypt
from models.engine.dbstorage import MongoDBClient

def hashpassword(password):
    """"""

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), salt)

    return hashed_password

def _generate_uuid():
    """"""

    new_id = str(uuid.uuid4())
    return new_id


class Auth:
    """"""

    def __init__(self):
        """"""

        self._id = MongoDBClient()


    def reg_email(self, col, email, password, first_name, last_name, age, session_id=None):
        """"""

        try:
            user = self._id.find_one(col, {"email": email})
            if user:
                raise ValueError(f"User {email} already exists")
            check = hashpassword(password)
            data = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "age": age,
                    'email': email,
                    'password': check,
                    'session_id': session_id
                    }
            return self._id.insert_one(col, data)
        except PyMongoError as e:
            print(f"Error registering user: {str(e)}")
            raise e

    def valid_login(self, col, email, password):
        """"""

        try:
            user = self._id.find_one(col, {"email": email})
            if user is None:
                raise ValueError(f"User {email} does not exists")
            if not bcrypt.checkpw(password.encode('utf-8'),
                user['password']):
                return False
            return True
        except PyMongoError as e:
            return False

    def createSession(self, col, email):
        """"""

        try:
            user = self._id.find_one(col, {"email": email})
            if user:
                new_id = _generate_uuid()
                result = self._id.update_one(col, {"_id": user["_id"]}, {"session_id": new_id})
                if result > 0:
                    return new_id
                else:
                    print("No documents matched the query")
            else:
                return None
        except PyMongoError as e:
            print(f"Error creating session: {str(e)}")
            return None


    def get_user_from_session_id(self, col, session_id):
        """"""

        if session_id is None:
            return None

        try:
            user = self._id.find_one(col, {"session_id": session_id})
            if user is None:
                return None
            return user
        except PyMongoError as e:
            print(f"Error retrieving user by session ID: {str(e)}")
            return None

    def destroy_session(self, col, email):
        """"""

        try:
            user = self._id.find_one(col, {"email": email})
            result = self._id.update_one(col, {"_id": user["_id"]}, {"session_id": None})
            if result > 0:
                n_user = user["_id"]
                print(f"Session destroyed for user {n_user}.")
                return True
            return False
        except PyMongoError as e:
            print(f"Error destroying session: {str(e)}")
            return False


    def get_reset_password_token(self, col, email):
        """"""

        try:
            user = self._id.find_one(col, {"email": email})
            if user is None:
                raise ValueError(f"User {email} does not exist")
            new_id = _generate_uuid()
            self._id.update_one(col, {"_id": user["_id"]}, {"reset_token": new_id})
            return new_id
        except PyMongoError as e:
            print(f"Error generating reset token: {str(e)}")
            return None

    def update_password(self, col, reset_token, password):
        """"""

        try:
            user = self._id.find_one(col, {"reset_token": reset_token})
            if user is None:
                raise ValueError("Invalid reset token")
            hashed_password = hashpassword(password)
            self._id.update_one(col, {"_id": user["_id"], "password": hashed_password}, {"reset_token": None})
            print("Password updated successfully.")
        except PyMongoError as e:
            print(f"Error updating password: {str(e)}")

    def update_account(self, col, old_email, firstName, lastName, age, email, password):
        """"""

        try:
            user = self._id.find_one(col, {"email": old_email})
            if user is None:
                raise ValueError("User not exists")
            check = hashpassword(password)
            result = self._id.update_one(col, {"_id": user['_id']}, {"firstName": firstName, "lastName": lastName, "age": age, "email": email, "password": check})
            if result > 0:
                return({"firstName": firstName, "lastName": lastName, "age": age, "email": email, "password": check})
            return None
        except PyMongoError as e:
            print(f"Error updating user info: {str(e)}")
            raise e
