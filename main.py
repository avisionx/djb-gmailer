import email
import imaplib
import os
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from textwrap import dedent

from dotenv import load_dotenv

from helpers import ComplaintParser

load_dotenv()

# NOTE: ALLOW LESS SECURE APPS IN GMAIL
SECRET_EMAIL = os.getenv("SECRET_EMAIL")
SECRET_PWD = os.getenv("SECRET_PWD")


class Gmailer:

    IMAP_SERVER = "imap.gmail.com"
    SMTP_SERVER = "smtp.gmail.com"

    def __init__(self, email, pwd):
        self.email = email
        self.pwd = pwd
        with open("body_main.txt", 'r') as body_main:
            self.body_main = body_main.read()
        with open("body_redressal.txt", 'r') as body_redressal:
            self.body_redressal = body_redressal.read()

    def __str__(self):
        return self.email

    def __getOriginalEmailData(self, msg):
        id = msg['Message-ID']
        email_from = msg['From']
        email_subject = msg['Subject']
        email_datetime = email.utils.parsedate_to_datetime(msg["Date"])

        email_date = email_datetime.strftime("%d/%m/%Y")
        email_time = email_datetime.strftime("%H:%M:%S")

        email_body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    email_body += body
        else:
            content_type = msg.get_content_type()
            body = msg.get_payload(decode=True).decode()
            if content_type == "text/plain":
                email_body += body

        return {
            'id': id,
            'email_from': email_from,
            'email_subject': email_subject,
            'email_date': email_date,
            'email_time': email_time,
            'email_body': email_body
        }

    def __create_auto_reply(self, original, redressal=False):
        mail = MIMEMultipart('alternative')
        mail['Message-ID'] = make_msgid()
        mail['References'] = mail['In-Reply-To'] = original['id']
        mail['Subject'] = 'Re: ' + original['email_subject']
        mail['From'] = self.email
        mail['To'] = original['email_from']
        if redressal:
            mail.attach(MIMEText(dedent(self.body_redressal), 'plain'))
        else:
            mail.attach(MIMEText(dedent(self.body_main), 'plain'))
        return mail

    def __replyToEmail(self, original):
        complaintParser = ComplaintParser()
        complaint_params, redressal = complaintParser.parse(
            original['email_body'])
        with smtplib.SMTP_SSL(self.SMTP_SERVER) as conn:
            conn.login(self.email, self.pwd)
            conn.sendmail(
                self.email,
                [original['email_from']],
                self.__create_auto_reply(original, redressal).as_bytes()
            )
        
        if not redressal:
            print(complaint_params, original)

    def reply_unread_emails(self):

        conn = imaplib.IMAP4_SSL(self.IMAP_SERVER)

        try:
            (retcode, capabilities) = conn.login(self.email, self.pwd)
        except:
            print(sys.exc_info()[1])
            sys.exit(1)

        conn.select()
        (retcode, messages) = conn.search(
            None, 'X-GM-RAW', r'"in:inbox is:unread"')

        if(retcode == 'OK'):
            messageList = list(map(int, messages[0].split()))
            for uid in messageList:
                typ, data = conn.fetch(str(uid), '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        originalEmailData = self.__getOriginalEmailData(msg)
                        self.__replyToEmail(originalEmailData)
                typ, data = conn.store(str(uid), '+X-GM-LABELS', 'replied')


if __name__ == "__main__":
    gmailer = Gmailer(SECRET_EMAIL, SECRET_PWD)
    gmailer.reply_unread_emails()
