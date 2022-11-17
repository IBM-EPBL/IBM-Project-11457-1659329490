import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import dotenv

dotenv.load_dotenv()


def sent_mail(subject, content):
    message = Mail(
        from_email="737819CSR154@smartinternz.com",
        to_emails="raveencr2@gmail.com",
        subject=subject,
        html_content=content,
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
