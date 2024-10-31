#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
import logging

logging.basicConfig(level=logging.DEBUG)
"""if not MongoDBClient().is_connected():
    print("MongoDB connection failed!")"""

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    auth = Auth()
    col = MongoDBClient().createCollection("user")

    logging.debug(f"Request data: {request.json}")
    data = request.get_json()
    print(f"Received data: {data}")
    first_name = data.get('firstName')
    lastname = data.get('lastName')
    age = data.get('age')
    email = data.get('email')
    password = data.get('password')

    if not data:
        return jsonify({"error": "Invalid Json"}), 400
    logging.debug(f"This is current collection({col})")
    if not email or not password:
        return jsonify({"error": "email or password missing"}), 400
    try:
        print(f"Input Data: {data}")
        user = auth.reg_email(col, email, password, first_name, lastname, age)
        session_id = auth.createSession(col, email)
        if session_id is None:
            return jsonify({"error": "Failed to create session"}), 500
        res = make_response(jsonify({"email": email, "session_id": session_id, "message": "logged in"}))
        res.set_cookie('session_id', session_id, max_age=24*60*60)
        return res
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        logging.error("User creation failed due to some condition")
        return jsonify({"error": "Failed to create user"}), 500

@app_views.route('/login', methods=['POST'], strict_slashes=False)
def valid_user():
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    auth = Auth()
    col = MongoDBClient().createCollection("user")

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "email or password missing"}), 400
    try:
        sign_in = auth.valid_login(col, email, password)
        if not sign_in:
            abort(401, description="Password does not exist")
        session_id = auth.createSession(col, email)
        if session_id is None:
            return jsonify({"error": "Failed to create session"}), 500
        res = make_response(jsonify({"email": email, "session_id": session_id, "message": "logged in"}))
        res.set_cookie('session_id', session_id, max_age=24*60*60)
        return res
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        abort(500)


@app_views.route('/session/<session_id>', methods=['GET'], strict_slashes=False)
def get_session(session_id):
    """"""
    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    auth = Auth()
    col = MongoDBClient().createCollection("user")

    if session_id is None:
        return jsonify({"error": "Failed to create session"}), 500
    try:
        user = auth.get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "Invalid session ID"}), 401
        return jsonify({"email": user["email"], "firstName": user["firstName"], "message": "logged in"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        logging.error(f"Error found while retrieving {str(e)}")
        abort(500)

@app_views.route('/updateAccount/<session_id>', methods=['PUT'], strict_slashes=False)
def update_account(session_id):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    auth = Auth()
    col = MongoDBClient().createCollection("user")
    
    data = request.get_json()
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    age = data.get('age')
    password = data.get('password')

    if session_id is None:
        return jsonify({"error": "Failed to retrieve session"}), 500
    try:
        user = auth.get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "Invalid session ID"}), 401
        logging.debug(f"check if user sessdion exists {user}")

        ndict = {
                "firstName": firstName, "lastName": lastName, "age": age, "email": email, "password": password, "session_id": session_id}
        if user == ndict:
            return jsonify({"message": "updated successfully"}), 200
        result = auth.update_account(col, user['email'], firstName, lastName, age, email, password)
        logging.debug(f"Check result resolve {result}")
        if not result:
            return jsonify({"error": "could not update account"}), 401
        return jsonify({"resut": result.get("email"), "message": "Account updated succesfully"}), 200
    except Exception as e:
        logging.error(f"Exception occurred during account update: {e}")
        return jsonify({"error": "An error occurred during update"}), 500

@app_views.route('/logout/<session_id>', methods=['DELETE'], strict_slashes=False)
def logout_account(session_id):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    auth = Auth()
    col = MongoDBClient().createCollection("user")

    if session_id is None:
        return jsonify({"error": "Failed to retrieve session"}), 500

    try:
        user = auth.get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "Invalid session ID"}), 401
        result = auth.destroy_session(col, user['email'])
        if result > 0:
            return jsonify({"message": "logout successfully"})
        return jsonify({"error": "Error logging out"})

    except Exception as e:
       logging.error(f"Could not result error {e}")
       return jsonify({"error": "check error "}), 500


@app_views.route('/accountInfo/<session_id>', methods=['GET'], strict_slashes=False)
def account_info(session_id):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    auth = Auth()
    col = MongoDBClient().createCollection("user")

    if session_id is None:
        return jsonify({"error": "Failed to retrieve session"}), 500

    try:
        user = auth.get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "Invalid session ID"}), 401
        return jsonify({"firstName": user["firstName"],
            "lastName": user["lastName"],
            "age": user["age"],
            "email": user["email"],
            "message": "Account info retrieval was successful"}), 200
    except Exception as e:
        logging.error(f"Could not result error {e}")
        return jsonify({"error": "check error "}), 500
