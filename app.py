import os

import jsonlines
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_basicauth import BasicAuth

from main import Gmailer

load_dotenv()

COMPLAINTS_FILE = 'complaints.jsonl'
with open(COMPLAINTS_FILE, 'a+') as COMPLAINTS_FILE_OBJ:
    COMPLAINTS_FILE_OBJ.close()

# NOTE: ALLOW LESS SECURE APPS IN GMAIL
SECRET_EMAIL = os.getenv("SECRET_EMAIL")
SECRET_PWD = os.getenv("SECRET_PWD")
BASIC_AUTH_REALM = os.getenv("BASIC_AUTH_REALM")
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")

app = Flask(__name__)

app.config['BASIC_AUTH_REALM'] = BASIC_AUTH_REALM
app.config['BASIC_AUTH_USERNAME'] = BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = BASIC_AUTH_PASSWORD

basic_auth = BasicAuth(app)

# Create a cron job like so crontab -e add this
# * * * * * /opt/local/bin/curl -X GET https://falken:joshua@YOUR_APP/cron/do_the_thing
@app.route('/cron/email', methods=['GET'])
@basic_auth.required
def reply_unread_emails():
    gmailer = Gmailer(SECRET_EMAIL, SECRET_PWD)
    gmailer.reply_unread_emails()
    return "success"

@app.route('/emails', methods=['GET'])
@basic_auth.required
def emails():
    complaints_list = []
    with jsonlines.open(COMPLAINTS_FILE, mode='r') as reader:
        for obj in reader.iter(type=dict, skip_empty=True, skip_invalid=True):
            complaints_list.append(obj)
    return jsonify(complaints_list)
