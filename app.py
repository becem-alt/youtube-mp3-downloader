from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return   render_template('home.html')


@app.route('/download', methods=['POST'])
def login():
    return render_template('download.html',url=request.form['url'])
