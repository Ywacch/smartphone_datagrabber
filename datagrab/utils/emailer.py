import smtplib
import codecs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datagrab import eBay_API_metrics, email_log


def send_mail():
    """

    :return:
    """
    email = 'ywacch@gmail.com'

    msg = MIMEMultipart('alternative')

    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Zeldr datagrab daily report'
    email_body = "Here are the reports of today's dataget.\n More info can be seen in the mongo cluster"

    msg.attach(MIMEText(email_body, 'plain'))

    # make another database for stored_listings (too big for google)
    send_files = {'api_metrics.json': eBay_API_metrics, 'email_log.json': email_log} #, 'stored_listings.json': temp_listings_store}

    for filename, file in send_files.items():
        jfile = codecs.open(file, "r", "utf-8")
        attachment = MIMEText(jfile.read())
        attachment.add_header('Content-Disposition', 'attachment',
                              filename=filename)
        msg.attach(attachment)

    with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465) as smtp:
        smtp.login(email, 'bdmnjbarordmunuc')  # use env variables for security
        smtp.send_message(msg)
