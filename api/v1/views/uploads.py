#!/usr/bin/python3
""""""
import base64
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from api.v1.auth.file_auth import File
import logging

logging.basicConfig(level=logging.DEBUG)

@app_views.route('/uploadprofilepic/<session_id>', methods=['POST'], strict_slashes=False)
def upload_profile_pic(session_id):
    try:
        from api.v1.auth.user_auth import Auth
        from models.engine.dbstorage import MongoDBClient
        col = MongoDBClient().createCollection("pictures")
        use = MongoDBClient().createCollection("user")

        data = request.get_json()
        if not data or 'profile_pic' not in data:
            return jsonify({"error": "No file part in the request"}), 400
        user = Auth().get_user_from_session_id(use, session_id)
        if not user:
            return jsonify({"error": "invalid user"}), 500

        pic = MongoDBClient().find_one(col, {"email": user['email']})
        if not pic:
            data = {
                    "email": user['email'],
                    "profile_pic": data['profile_pic']
                    }
            MongoDBClient().insert_one(col, data)
            return jsonify({"status": "success", "message": "Profile picture uploaded successfully"})
        folders = MongoDBClient().update_one(col,
            {'_id': pic['_id']},
            {'profile_pic': data['profile_pic']}
        )
        if pic['profile_pic'] == data['profile_pic']:
            return jsonify({"status": "success", "message": "Profile picture is already up to date"}), 200
        logging.debug(f"Modified count after update: {folders}")
        if folders > 0:
            return jsonify({"status": "success", "message": "Profile picture updated successfully"})
        else:
            return jsonify({"error": "Failed to update profile picture"}), 500
    except Exception as e:
        logging.error(f"Error updating profile picture: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app_views.route('/delete_profile_pic/session_id', methods=['DELETE'])
def delete_profile_pic(session_id):
    image_data = request.files['profile_pic'].read()
    
    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")

    encoded_image = None
    try:
        user = Auth().get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "invalid user"}), 500
    
        folders = MongoDBClient().delete_one(
            {'_id': user['_id'], 'profile_picture': encoded_image}
        )
    
        if folders > 0:
            return jsonify({"status": "success", "message": "Profile picture uploaded successfully"})
        else:
            return jsonify({"error": "Failed to update profile picture"}), 500
    except Exception as e:
        logging.error(f"Error updating profile picture: {e}")
        return jsonify({"error": "Internal server error"}), 500
