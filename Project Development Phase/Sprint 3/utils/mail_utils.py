import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, To, Content, Mail
import sendgrid
import dotenv
from flask import flash

dotenv.load_dotenv()


def sent_mail(email, subject, content):
    message = Mail(
        from_email="raveencr2@gmail.com",
        to_emails=email,
        subject=subject,
        html_content=content,
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        flash("Mail sent successfully")
    except Exception as e:
        print(e)
        flash("Can't sent mail", "error")
