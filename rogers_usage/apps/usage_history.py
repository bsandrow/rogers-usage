
import argparse
import csv
import datetime
import getpass
import smtplib
import socket
import StringIO
import sys

from email.mime.text      import MIMEText
from email.mime.multipart import MIMEMultipart

from rogers_usage.auth import get_auth_info
from rogers_usage.session import RogersSession
import rogers_usage.usage as usage

address_default = "%s@%s" % ( getpass.getuser(), socket.gethostname() )

def usage_history_csv(session, csv_options=None):
    """ Fetch usage history for previous months. Return in csv format. """
    csv_options = csv_options or {}
    data = usage.previous_monthly_usage(session)
    output = StringIO.StringIO()
    writer = csv.writer(output, **csv_options)

    for row in data:
        writer.writerow(row)

    return output.getvalue()

def build_email(csv_data, recipients, sender):
    """ Build an email with :csv_data: attached as a .csv file """

    subject_timestamp = datetime.datetime.now().strftime("%Y-%B-%d %H:%M")

    msg = MIMEMultipart()
    msg['Subject'] = 'Rogers Usage History [%s]' % (subject_timestamp)
    msg['From']    = sender
    msg['To']      = recipients

    text_container = MIMEMultipart('alternative')
    text_part = MIMEText("""
        Attached is a CSV showing the bandwidth usage history of this Rogers
        account over the past few months.

        Note: The current month is excluded since it is still open.
        """, 'plain')
    text_container.attach(text_part)

    filename_timestamp = datetime.datetime.now().strftime("%Y%m%d")
    filename = 'rogers_usage_history_%s.csv' % (filename_timestamp)
    csv_part = MIMEText(csv_data, 'csv')
    csv_part.add_header('Content-Disposition', 'attachment', filename=filename)

    msg.attach(text_container)
    msg.attach(csv_part)

    return msg

def parse_arguments():
    """ Parse command-line arguments """
    parser = argparse.ArgumentParser(description="""
        blah blah blah""")

    parser.add_argument('-r', '--recipients', default=address_default,
                        help=""" Comma-separated list of email addresses to
                        send the report to. (default: %s)""" % (address_default))
    parser.add_argument('-f', '--from', dest='from_addr', default=address_default,
                        help=""" The email address that the report will be sent
                        from. (default: %s)""" % (address_default) )
    parser.add_argument('-s', '--smtp', default='localhost',
                        help=""" The SMTP host to send the email through.
                        (default: localhost) """)

    options = parser.parse_args()
    return options

def main():
    """ main """
    options = parse_arguments()
    authinfo = get_auth_info()
    session = RogersSession(authinfo.username, authinfo.password)
    csv_data = usage_history_csv(session)
    message = build_email(csv_data, options.recipients, options.from_addr)

    smtplib.SMTP(options.smtp).sendmail(options.from_addr, options.recipients, message.as_string())

def run():
    """ Wrapper around main() for exception handling """
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(">> Caught user interrupt. Exiting...")

if __name__ == '__main__':
    run()

# def daily_breakdown_csv(session, csv_options):
#     breakdown = usage.current_month_daily_breakdown(session)
#     output = StringIO.StringIO()
#     writer = csv.writer(output, **(csv_options or {}))
# 
#     for row in breakdown.data:
#         writer.writerow(row)
# 
#     return output.getvalue()
