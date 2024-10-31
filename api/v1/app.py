#!/usr/bin/python3
""""""
import logging
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])
app.register_blueprint(app_views)
CORS(app, resources={r'/api/v1/*': {"origins": "*"}})


@app.route('/', methods=['GET'], strict_slashes=False)
def ccheck_form():
    """"""

    return jsonify({"message": "Welcome to LibPredict"})

if __name__ == '__main__':
    port = 5001
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=True)
