#!/usr/bin/env python

import argparse
import datetime
import getpass
import json
import os
import smtplib
import socket
import sys

from email.mime.text import MIMEText

from xdg.BaseDirectory import load_first_config

from rogers_usage.session import RogersSession
from rogers_usage.usage   import current_usage_info

# User Options:
#   - Account Credentials for the My Rogers account (username/password).
#   - "From:" address for the email.
#   - The recipients of the email.
#   - The SMTP host to sent the email through.

address_default = "%s@%s" % ( getpass.getuser(), socket.gethostname() )

def draft_email(info, from_addr, to_addrs):
    """ Create an email from BW usage info. """

    msg = MIMEText("""\
Rogers Bandwidth Usage
======================

Total Usage    : %(total_usage)s GB
    Downloads  : %(download_usage)s GB
    Uploads    : %(upload_usage)s GB

Usage Allowance: %(allowance)s GB
Usage Left     : %(left)s GB

Note:
- For period %(billing_period)s.
- Usage information may be up to 48 hours old.

""" % info)

    msg['Subject'] = 'Rogers Bandwidth Usage [%s]' % (datetime.datetime.now().strftime("%Y-%B-%d %H:%M"))
    msg['To']      = to_addrs
    msg['From']    = from_addr

    return msg

def parse_args():
    parser = argparse.ArgumentParser(description="""
        Send an email summarizing Rogers bandwidth usage for the current
        period.
        """)

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

def read_auth():
    config_dir = load_first_config('rogers-usage')
    with open(os.path.join(config_dir, 'auth.json'), 'rb') as fh:
        return json.loads(fh.read()) or {}

def main():
    options = parse_args()
    auth    = read_auth()
    session = RogersSession(auth['username'], auth['password'])
    info    = current_usage_info(session)
    msg     = draft_email(info, options.from_addr, options.recipients)

    smtplib.SMTP(options.smtp).sendmail(options.from_addr, options.recipients, msg.as_string())

def run():
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(">> Caught user interrupt. Exiting...")
