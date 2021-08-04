
#this file contains methods that help send emails with gmail account

from threading import Thread
#from website.models import UserCommon as User
from flask import abort, flash, render_template
from datetime import datetime
from flask_mail import Message
from server.api.extensions import gmail_client
from server.api.models import Confirmation_Email_Message
import os


def _send_async_emails(messages):
    from server.api import create_app
    my_app = create_app(os.getenv("PROJECT_MODE", "production"))
    my_app.app_context().push()
    for one_message in messages:
        try:
            gmail_client.send(one_message)
        except:
            pass



def send_emails(from_email, to_emails, subject, template, **kwargs):
    msgs = []
    for one_recipient in to_emails:
        msg = Message(subject=subject, sender=from_email, recipients=[one_recipient],
                      #body=render_template(template + '.txt', **kwargs),
                      html=render_template(template + '.html', **kwargs)
                      )
        msgs.append(msg)

    t = Thread(target=_send_async_emails, args=[msgs])
    t.start()
    return t


#FIXME: need
def send_event_emails(from_email, to_emails, subject, body):
    msgs = []
    for one_recipient in to_emails:
        msg = Message(subject=subject, sender=from_email, recipients=[one_recipient],
                      body=body
                      )
        msgs.append(msg)

    t = Thread(target=_send_async_emails, args=[msgs])
    t.start()
    return t

#send confirmation emails to littles: they are paired
def send_little_confirm_emails(email_list, additional_messages="Don't forget about the reveals!!", name="n/a"):
    db_additional_message = Confirmation_Email_Message.query.first()
    if db_additional_message:
        additional_messages = db_additional_message.message
    send_emails(
        from_email=os.getenv('MAIL_USERNAME'),
        to_emails=email_list,
        subject="Congratulations! You Are Paired",
        #message="sorry about this late email, but the due date of A1 is changed to tomorrow, remmeber to bring your homework tomorrow moring!!!"
        template='emails/little_confirm',
        name=name,
        additional_messages=additional_messages,
        timestamp=datetime.now().strftime('%b-%d-%I%M%p-%G')
    )



def send_big_confirm_emails(email_list, additional_messages="Don't forget about the reveals!!", name="n/a", result_list="n/a"):
    db_additional_message = Confirmation_Email_Message.query.first()
    if db_additional_message:
        additional_messages = db_additional_message.message

    send_emails(
        from_email=os.getenv('MAIL_USERNAME'),
        to_emails=email_list,
        subject="Congratulations! You Are Paired",
        #message="sorry about this late email, but the due date of A1 is changed to tomorrow, remmeber to bring your homework tomorrow moring!!!"
        #template='emails/big_confirm',
        template='emails/answers_table',
        name=name,
        result_list=result_list,
        additional_messages=additional_messages,
        timestamp=datetime.now().strftime('%b-%d-%I%M%p-%G')
    )



