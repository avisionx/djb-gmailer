import os

from dotenv import load_dotenv
from flask import Flask
from flask_basicauth import BasicAuth

from main import Gmailer

load_dotenv()

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
