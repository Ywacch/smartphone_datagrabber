import smtplib
import codecs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml

from datagrab import datagrab_log, email_log, email_config


def parse_config():
    try:
        with open(email_config, 'r') as file:
            parsed_yml = yaml.load(file, Loader=yaml.FullLoader)
            return parsed_yml
    except FileNotFoundError:
        datagrab_log.error(f" Config file not found. Please insert a file named {email_config} in the database/datafiles directory")
    except Exception as e:
        datagrab_log.error(f"Error occurred at db_config: {e}")


def send_mail():
    """

    :return:
    """
    email_params = parse_config()

    if not email_params:
        return
    
    email = email_params['username']
    password = email_params['password']

    msg = MIMEMultipart('alternative')

    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Smartphone market datagrab daily report'
    email_body = "Here are the reports of today's data collection operations."

    msg.attach(MIMEText(email_body, 'plain'))

    # make another database for stored_listings (too big for google)
    send_files = {'datagrab.log': datagrab_log, 'smartphones.log': email_log}

    for filename, file in send_files.items():
        jfile = codecs.open(file, "r", "utf-8")
        attachment = MIMEText(jfile.read())
        attachment.add_header('Content-Disposition', 'attachment',
                              filename=filename)
        msg.attach(attachment)

    with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465) as smtp:
        smtp.login(email, password)  # use env variables for security
        smtp.send_message(msg)
