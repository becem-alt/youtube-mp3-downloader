from flask import Flask
from flask import render_template
from flask import request
import os
app = Flask(__name__)


@app.route("/")
def hello_world():
    return   render_template('home.html')


@app.route('/download', methods=['POST'])
def download():
    os.system(f"yt-dlp -x  --audio-format mp3 {request.form['url']}")
    return render_template('download.html',url=request.form['url'])
