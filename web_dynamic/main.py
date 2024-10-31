#!/usr/bin/python3
""""""

from flask import Flask, render_template
app = Flask(__name__, static_url_path='/static')

@app.route('/LibPredict', strict_slashes=False)
def landingpage():
    return render_template('landingpage.html')

@app.route('/LibPredict/signup', strict_slashes=False)
def signup():
    return render_template('signup.html')

@app.route('/LibPredict/mainapp', strict_slashes=False)
def mainapp():
    return render_template('mainapp.html')

@app.route('/LibPredict/folders', strict_slashes=False)
def folder():
    return render_template('folder.html')

@app.route('/LibPredict/files', strict_slashes=False)
def file():
    return render_template('files.html')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
