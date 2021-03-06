import smtplib
import sys

sys.path.append('/home/pi/project')
import log

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = log.get_logger()


def write_letter(text, email, url):
    fromaddr = "basicsensorsystem@gmail.com"
    toaddr = email
    mypass = "dragondragon"

    msg = MIMEMultipart()
    msg['From'] = url
    msg['To'] = email
    msg['Subject'] = "Warning!"

    body = text
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    logger.info('Notification sent')
