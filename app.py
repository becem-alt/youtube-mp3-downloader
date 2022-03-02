from subprocess import Popen
import subprocess
from flask import Flask
from flask import render_template
from flask import request
import os
import re

app = Flask(__name__)



@app.route("/")
def hello_world():
    return   render_template('home.html')


@app.route('/download', methods=['POST'])
def download():
   
    p = Popen(f"yt-dlp --restrict-filenames  -x --no-playlist -o '%(title)s.%(ext)s' --audio-format mp3 {request.form['url']}", shell=True, stdout=subprocess.PIPE,
              stderr=subprocess.PIPE, universal_newlines=True)

    output, errors = p.communicate()
    name=output.split('\n')[-3].replace('[ExtractAudio] Destination: ', '')
    p = Popen(f'aws s3 cp {name}  s3://becem-youtube-app  --content-disposition=attachment',shell=True)
    p.wait()
    print('COMPLETED')
    writeLogs(output)
    #os.system(f"aws s3 cp b.mp3 s3://becem-youtube-app  --content-disposition=attachment")
    url = "https://becem-youtube-app.s3.eu-west-3.amazonaws.com/"+name
    return render_template('download.html', url=url)


def writeLogs(logs):
    f = open('logs.txt', 'a')
    f.write("**********************************************************************************************\n")
    f.write(logs)
    f.write("**********************************************************************************************\n\n\n\n")
    f.close()
