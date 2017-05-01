import json
try:
    import yagmail
except ImportError as e:
    print("Error importing yagmail. Check out https://github.com/kootenpv/yagmail#install for installation.", e)
try:
    import phonenumbers
except ImportError as e:
    print("Error importing phonenumbers.", e)


class MailToSMS:
    """MailToSMS

    This module implements a basic api for sending text messages via email using yagmail.

    Requirements:
        yagmail
        phonenumbers

        Install with pip install -r requirements.txt

    Arguments:
        number {string|int}: The destination phone number (ex. 5551234567)
        carrier {string}: The destination phone number's carrier (ex. "att")
        username {string}: The username for accessing the SMTP server (ex. "username")
        password {string}: The password for accessing the SMTP server (ex. "password")
            If using Gmail and 2FA, you may want to use an app password.
        contents {yagmail contents}: A yagmail friendly contents argument (ex. "This is a message.")
            See: https://github.com/kootenpv/yagmail#magical-contents
        keyword args: A set of optional kwargs for extra configuration.
            region {string}: The region of the destination phone number. Defaults to "US". (ex. region="US")
                This should only be necessary when using a non international phone number that's not US based.
                See: https://github.com/daviddrysdale/python-phonenumbers
            subject {string}: The subject of the email to send (ex. subject="This is a subject.")
            yagmail {list}: A list of arguments to send to the yagmail.SMTP() constructor. (ex. yagmail=["my.smtp.server.com", "12345"])
                As of 4/30/17, the args and their defaults (after the username and password) are:
                    host='smtp.gmail.com', port='587', smtp_starttls=True, smtp_set_debuglevel=0, smtp_skip_login=False, encoding="utf-8"
                This is unnecessary if you're planning on using the basic Gmail interface, 
                    in which case you'll just need the username and password.
                See: https://github.com/kootenpv/yagmail/blob/master/yagmail/yagmail.py#L49

    Examples:
        MailToSMS(5551234567, "att", "username@gmail.com", "password", "contents string!")
        MailToSMS(5551234567, "att", "username@gmail.com", "password", ["contents line one", "contents line two"], subject="subject string!")
        MailToSMS(5551234567, "att", "username@gmail.com", "password", "contents string!", yagmail=["smtp.gmail.com", "587"])
    """

    ## Config
    GATEWAYS_JSON_PATH = "gateways.json"
    GATEWAYS_KEY = "gateways"
    CARRIER_KEY = "carrier"
    SMS_KEY = "sms"
    MMS_KEY = "mms"
    DEFAULT_REGION = "US"


    def __init__(self, number, carrier, username, password, contents, **kwargs):
        self.static = MailToSMS

        self.gateways = self.load_gateways()
        if(not self.gateways):
            return

        number = self.validate_number(number, kwargs.get("region", self.static.DEFAULT_REGION))
        carrier = self.validate_carrier(carrier)
        if(not number or not carrier):
            return

        gateway = self.get_gateway(carrier)
        if(not gateway):
            return

        ## Prepare the args for yagmail
        yagmail_args = kwargs.get("yagmail", [])

        ## Prepare kwargs for yagmail
        yagmail_kwargs = {}
        yagmail_kwargs["to"] = "{0}@{1}".format(number, gateway)
        if(kwargs.get("subject", False)):
            yagmail_kwargs["subject"] = kwargs["subject"]
        yagmail_kwargs["contents"] = contents

        ## Init the yagmail connection
        try:
            connection = yagmail.SMTP(username, password, *yagmail_args)
        except Exception as e:
            ## You might want to look into using an app password for this.
            print("Unhandled error creating yagmail connection.\nSee the following error text:", e)
            return

        ## Send the mail
        try:
            connection.send(**yagmail_kwargs)
        except Exception as e:
            print("Unhandled error sending mail", e)
            return


    def load_gateways(self):
        with open(self.static.GATEWAYS_JSON_PATH, "r") as fd:
            try:
                return json.load(fd)[self.static.GATEWAYS_KEY]
            except Exception as e:
                print("Unhandled error loading gateways.json", e)
                return []


    def validate_number(self, number, region):
        number = str(number)

        try:
            parsed = phonenumbers.parse(number, region)
        except phonenumbers.phonenumberutil.NumberParseException as e:
            print("NumberParseException when parsing the phone number", e)
            return 0
        except Exception as e:
            print("Unhandled error when parsing the phone number", e)
            return 0

        else:
            if (phonenumbers.is_possible_number(parsed) and 
                phonenumbers.is_valid_number(parsed)):
                return number
            else:
                print("{0} isn't a valid phone number.".format(number))
                return 0


    def validate_carrier(self, carrier):
        for gateway in self.gateways:
            if(gateway[self.static.CARRIER_KEY] == carrier):
                return carrier
        else:
            print("{0} isn't a valid carrier.".format(carrier))
            return ""


    def get_gateway(self, carrier):
        for gateway in self.gateways:
            if(gateway[self.static.CARRIER_KEY] == carrier):
                ## Return sms gateway if possible, else return the mms gateway
                if(gateway[self.static.SMS_KEY]):
                    return gateway[self.static.SMS_KEY]
                elif(gateway[self.static.MMS_KEY]):
                    return gateway[self.static.MMS_KEY]
                else:
                    print("{0} doesn't have a SMS or MMS gateway defined.".format(carrier))
                    return ""
        else:
            print("{0} doesn't have any valid gateways.".format(carrier))   # This shouldn't happen.
            return ""
