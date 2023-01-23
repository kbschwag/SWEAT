import smtplib
import jinja2
from os import getenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# this will connect to email server when decided
if getenv('FLASK_ENV') == 'development':
    try:
        mailer = smtplib.SMTP('localhost', 1025)
    except Exception as e:
        #If the dev mailer isn't available, send the mail to the console
        print("Falling back to demo mailer")
        class DemoMailer:
            def sendmail(self, _, dest, msg):
                print("Sending mail to", dest)
                print("Content:", msg)

        mailer = DemoMailer()
else:
    mailer = smtplib.SMTP('smtp.gmail.com', 587)
    mailer.starttls()
    mailer.auth('username', 'password')

SENDER = "mail@sweat.io"

def send_email(to, subject, content):
    """ Send email to user """
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'html'))
    mailer.sendmail(SENDER, to, msg.as_string())

# use jinja2 to render html templates
def send_templated_email(to, template, customizations):
    templateLoader = jinja2.FileSystemLoader(searchpath="mail")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template)
    content = template.render(customizations)
    send_email(to, customizations['subject'], content)
