import smtplib
import jinja2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# this will connect to email server when decided
mailer = smtplib.SMTP('localhost', 1025)
# mailer.auth('username', 'password')

SENDER = "mail@sweat.io"

def send_email(to, subject, content):
    """ Send email to user """
    # this will send email to user
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
