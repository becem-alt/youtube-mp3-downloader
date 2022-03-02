import imp
from subprocess import Popen
import subprocess
from flask import Flask
from flask import render_template, redirect, url_for, request
import time

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/message", methods=['POST'])
def saveMessage():
    message = {"name": request.form['name'],
               "company": request.form['company'],
               "telephone": request.form['telephone'],
               "email": request.form['email'],
               "message": request.form['message'],
                }
    writeMsgs(message)
    return redirect(url_for('home'))

@app.route('/download', methods=['POST'])
def download():
    p = Popen(f"yt-dlp --restrict-filenames  -x --no-playlist -o '%(title)s.%(ext)s' --audio-format mp3 {request.form['url']}", shell=True, stdout=subprocess.PIPE,
              stderr=subprocess.PIPE, universal_newlines=True)

    output, errors = p.communicate()
    name = output.split('\n')[-3].replace('[ExtractAudio] Destination: ', '')
    p = Popen(
        f'aws s3 cp {name}  s3://becem-youtube-app  --content-disposition=attachment', shell=True)
    p.wait()
    print('COMPLETED')
    writeLogs(output, request.form['url'])
    #os.system(f"aws s3 cp b.mp3 s3://becem-youtube-app  --content-disposition=attachment")
    url = "https://becem-youtube-app.s3.eu-west-3.amazonaws.com/"+name
    return render_template('download.html', url=url)


def writeLogs(logs,url):
    f = open('logs.txt', 'a')
    f.write(f"""**********************************************************************************************
Youtube video url : {url}
Time : {time.ctime()}
{logs}
**********************************************************************************************\n\n\n""")
    f.close()


def writeMsgs(msg):
    f = open('messages.txt', 'a')
    f.write(f"""**********************************************************************************************
Time : {time.ctime()}
Name : {msg['name']}
Company : {msg['company']}
Telephone : {msg['telephone']}
Email : {msg['email']}
Message : {msg['message']}
**********************************************************************************************\n\n\n""")
    f.close()

