import os

import jsonlines
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_basicauth import BasicAuth

from main import Gmailer

load_dotenv()

COMPLAINTS_FILE = 'complaints.jsonl'

# NOTE: ALLOW LESS SECURE APPS IN GMAIL
SECRET_EMAIL = os.getenv("SECRET_EMAIL")
SECRET_PWD = os.getenv("SECRET_PWD")
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = BASIC_AUTH_PASSWORD

basic_auth = BasicAuth(app)


def createFileIfNotExist(filename):
    with open(filename, 'a+') as outfile:
        outfile.close()

# Create a cron job like so crontab -e add this username and password from .env
# * * * * * /opt/local/bin/curl -X GET https://falken:joshua@YOUR_WEB_LINK/cron/email


@app.route('/cron/email', methods=['GET'])
@basic_auth.required
def reply_unread_emails():
    reply_redressal_url = 'https://jsonplaceholder.typicode.com/posts/1'
    reply_main_url = 'https://jsonplaceholder.typicode.com/posts/2'
    reply_redressal = requests.get(reply_redressal_url).json()['body']
    reply_main = requests.get(reply_main_url).json()['body']
    createFileIfNotExist(COMPLAINTS_FILE)
    gmailer = Gmailer(SECRET_EMAIL, SECRET_PWD)
    gmailer.reply_unread_emails(reply_main, reply_redressal)
    return "success"


@app.route('/emails', methods=['GET'])
@basic_auth.required
def emails():
    createFileIfNotExist(COMPLAINTS_FILE)
    complaints_list = []
    with jsonlines.open(COMPLAINTS_FILE, mode='r') as reader:
        for obj in reader.iter(type=dict, skip_empty=True, skip_invalid=True):
            complaints_list.append(obj)
    if os.path.exists(COMPLAINTS_FILE):
        os.remove(COMPLAINTS_FILE)
    return jsonify(complaints_list)
