from __future__ import print_function

from mail_to_sms import MailToSMS

import click


## See MailToSMS docstring for information about the arguments
@click.command()
@click.argument("phone-number", type=str)
@click.argument("carrier", type=str)
@click.argument("message", type=str)
@click.option("--yagmail-username", "-u", type=str, help="Specify a specific username for the SMTP server (ex. 'username'). Not necessary if a yagmail keyring and a .yagmail file are in use.")
@click.option("--yagmail-password", "-p", type=str, help="Specify a specific password for the SMTP server (ex. 'password'). Not necessary if a yagmail keyring and a .yagmail file are in use.")
def main(phone_number, carrier, message, yagmail_username, yagmail_password):
    MailToSMS(phone_number, carrier, yagmail_username, yagmail_password, message)

if(__name__ == "__main__"):
    main()