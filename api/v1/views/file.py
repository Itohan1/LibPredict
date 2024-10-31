#!/usr/bin/python3
""""""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from api.v1.auth.file_auth import File
import logging

logging.basicConfig(level=logging.DEBUG)

@app_views.route('/addfolder/<session_id>', methods=['POST'], strict_slashes=False)
def add_folder(session_id):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()

    data = request.get_json()
    folderName = data.get("folderName")
    if not session_id or not folderName:
        return jsonify({"error": "Failed to create session"}), 500
    try:
        user = Auth().get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "invalid user"}), 500

        reg = auth.reg_folder(fol, user["email"], folderName)
        return jsonify({"folderName": reg['folderName'], "message": "Folder has been formed"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        abort(500)

@app_views.route('/addfile/<session_id>', methods=['POST'], strict_slashes=False)
def add_file(session_id):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()

    data = request.get_json()
    folderName = data.get("folderName")
    file = data.get("file")
    if not session_id or not folderName:
        return jsonify({"error": "Failed to create session"}), 500
    try:
        user = Auth().get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "invalid user"}), 500
        check = auth.check_string(fil, folderName, file)
        reg = auth.reg_file(fil, user['email'], folderName, file)
        if check:
            return jsonify({"file": reg['file'], "exists": check[0], "generic": check[1], "message": "File has been formed"})
        return jsonify({"file": reg['file'], "message": "File has been formed"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        logging.error(f"error: {str(e)}")
        abort(500)

@app_views.route('/getFolders/<session_id>', methods=['GET'], strict_slashes=False)
def get_Folders(session_id):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()

    if not session_id:
        return jsonify({"error": "Failed to create session"}), 400
    try:
        user = Auth().get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "invalid user"}), 401
        folders = MongoDBClient().find_many(fol, {"email": user['email']})
        if not folders:
             return jsonify({"message": f"No folders has been created by {user['firstName']}"}), 200
        return jsonify([{"name": folder['folderName']} for folder in folders]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        abort(500)


@app_views.route('/getFiles/<folderName>', methods=['GET'], strict_slashes=False)
def get_Files(folderName):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()
    dlist = []

    try:
        files = MongoDBClient().find_many(fil, {"folderName": folderName})

        if not files:
             return jsonify([]), 200
        return jsonify([{"name": file['file']['name'], "content": file['file']['content'], "time": file['time']} for file in files]), 200
    except Exception as e:
        logging.error(f"Error retrieving files: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app_views.route('/findfolder/', methods=['GET'], strict_slashes=False)
def find_folder():
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()

    data = request.get_json()
    folderName = data.get("folderName")
    if not folderName:
        return jsonify({"error": "Folder name is missing"}), 400

    try:
        reg = auth.reg_folder(fol, folderName)
        if not reg:
            return jsonify({"error": "Failed to create folder"}), 404
        return jsonify({"folderName": reg['folderName'], "message": "Folder as been formed"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        abort(500)

@app_views.route('/findfile/<session_id>', methods=['GET'], strict_slashes=False)
def find_file(session_id):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()

    data = request.get_json()
    folderName = data.get("folderName")
    file = data.get("file")
    if not file:
        return jsonify({"error": "file name is missing"}), 400

    try:
        user = Auth().get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "invalid user"}), 401
        reg = auth.find_file(fol, user['email'], folderName, file)
        if not reg:
            return jsonify({"error": "Failed to create folder"}), 404
        return jsonify({"file": reg['file']['name'], "message": "Folder as been formed"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        abort(500)

@app_views.route('/findtime/<time>', methods=['GET'], strict_slashes=False)
def find_time(time):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()

    try:
        reg = auth.reg_file(fil, time)
        if not reg:
            return jsonify({"error": "Failed to create folder"}), 500
        for reg in reg:
            return jsonify({"folderName": reg['file'], "message": "File as been found"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        abort(500)

@app_views.route('/deletefolder/<session_id>', methods=['DELETE'], strict_slashes=False)
def delete_folder(session_id):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()

    data = request.get_json()
    folderName = data.get("folderName")
    if not session_id:
        return jsonify({"error": "Failed to create session"}), 400
    try:
        user = Auth().get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "invalid user"}), 401
        result = auth.delete_folder(fol, user['email'], folderName)
        if result is None:
            return jsonify({"error": f"Folder '{folderName}' not found"}), 404
        return jsonify({"message": "Folder as been deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        abort(500)

@app_views.route('/deletefile/<folderName>/<session_id>', methods=['DELETE'], strict_slashes=False)
def delete_file(folderName, session_id):
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()

    data = request.get_json()
    file = data.get("file")
    if not file:
        return jsonify({"error": "File name is missing"}), 400

    try:
        user = Auth().get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "invalid user"}), 401
        findit = MongoDBClient().find_one(fil, {"email": user['email'], "folderName": folderName})
        result = auth.delete_file(fil, user['email'], folderName, file)
        name = file['name']
        if result is None:
            return jsonify({"error": f"File '{name}' not found"}), 404
        return jsonify({"message": "File as been deleted"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        abort(500)

@app_views.route('/updatefolder', methods=['PUT'], strict_slashes=False)
def update_folder():
    """"""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()

    data = request.get_json()
    folderName = data.get("folderName")
    try:
        reg = auth.update_folder(fil, folderName)
        return jsonify({"folderName": reg["folderName"], "message": "Folder as been updated"})
    except Exception:
        abort(401)


@app_views.route('/variable', methods=['GET'], strict_slashes=False)
def variabele():
    """"""
    import os
    openai_api_key = os.getenv("OPENAI_API_KEY")

    return jsonify({"key": openai_api_key})


@app_views.route('/updateFile/<session_id>/<folderName>/<oldfile>', methods=['PUT'], strict_slashes=False)
def update_file(session_id, folderName, oldfile):
    """Update a file in a specific folder."""

    from api.v1.auth.user_auth import Auth
    from models.engine.dbstorage import MongoDBClient
    col = MongoDBClient().createCollection("user")
    fol = MongoDBClient().createCollection("folder")
    fil = MongoDBClient().createCollection("file")
    auth = File()

    data = request.get_json()
    new_file = data.get("file")

    if not session_id:
        return jsonify({"error": "Missing required session_id"})
    if not folderName:
        return jsonify({"error": "Missing required folderName"})
    if not oldfile:
        return jsonify({"error": "Missing required oldfile"})
    if not new_file:
        return jsonify({"error": "Missing required new file"}), 400

    try:
        user = Auth().get_user_from_session_id(col, session_id)
        if not user:
            return jsonify({"error": "invalid user"}), 401

        findit = MongoDBClient().find_one(fil, {"email": user['email'], "folderName": folderName, "file.name": oldfile})

        if not findit:
            raise ValueError(f"Could not find file '{old_file}' in folder '{folderName}' for user with email '{email}'")
        logging.debug('Could not find findiyt')

        result = MongoDBClient().update_one(fil, {"_id": findit["_id"]}, {"file.content": new_file['content']})
        if findit['file']['name'] == new_file['name']:
            return jsonify({"status": "success", "message": "Content has been edited"}), 200
        logging.debug(f"Modified count after update: {result}")
        if result > 0:
            return jsonify({"name": new_file['name'], "content": new_file['content'], "message": "File has been updated"}), 200
        return ({"error" : "It was not updated"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        abort(500, description="Could not connect with server")
