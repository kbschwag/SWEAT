import smtplib
import jinja2
from os import getenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# this will connect to email server when decided!
def get_mailer():
    if getenv('FLASK_ENV') == 'development':
        try:
            return smtplib.SMTP('localhost', 1025)
        except Exception as e:
            #If the dev mailer isn't available, send the mail to the console
            print("Falling back to demo mailer")
            class DemoMailer:
                def sendmail(self, _, dest, msg):
                    print("Sending mail to", dest)
                    print("Content:", msg)

                def quit(self):
                    pass

            return DemoMailer()
    else:
        mailer = smtplib.SMTP('email-smtp.us-east-2.amazonaws.com', 587)
        mailer.starttls()
        mailer.login(getenv('AWS_SES_USER'), getenv('AWS_SES_PASS'))
        return mailer

SENDER = "mail@tellsweat.com"

def send_email(to, subject, content):
    """ Send email to user """
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'html'))
    mailer = get_mailer()
    mailer.sendmail(SENDER, to, msg.as_string())
    mailer.quit()

# use jinja2 to render html templates
def send_templated_email(to, template, customizations):
    templateLoader = jinja2.FileSystemLoader(searchpath="website/mail")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template)
    content = template.render(customizations)
    send_email(to, customizations['subject'], content)
