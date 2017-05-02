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
        keyworded args (for extra configuration):
            region {string}: The region of the destination phone number. Defaults to "US". (ex. region="US")
                This should only be necessary when using a non international phone number that's not US based.
                See: https://github.com/daviddrysdale/python-phonenumbers
            mms {boolean}: Choose to send a MMS message instead of a SMS message, but will fallback to SMS if MMS isn't present. Defaults to False. (ex. mms=True)
            subject {string}: The subject of the email to send (ex. subject="This is a subject.")
            yagmail {list}: A list of arguments to send to the yagmail.SMTP() constructor. (ex. yagmail=["my.smtp.server.com", "12345"])
                As of 4/30/17, the args and their defaults (after the username and password) are:
                    host='smtp.gmail.com', port='587', smtp_starttls=True, smtp_set_debuglevel=0, smtp_skip_login=False, encoding="utf-8"
                This is unnecessary if you're planning on using the basic Gmail interface, 
                    in which case you'll just need the username and password.
                See: https://github.com/kootenpv/yagmail/blob/master/yagmail/yagmail.py#L49

    Examples:
        MailToSMS(5551234567, "att", "username@gmail.com", "password", "this is a message")

        MailToSMS("5551234567", "att", "username", "password", ["hello", "world"], subject="hey!")

        MailToSMS(5551234567, "att", "username", "password", "hello world!", yagmail=["smtp.gmail.com", "587"])

        MailToSMS("5551234567", "att", "username@gmail.com", "password", ["line one"], yagmail=["smtp.gmail.com"])

        mail = MailToSMS(5551234567, "att", "username", "password")
        mail.send("this is a string!")
    """

    ## Config
    GATEWAYS_JSON_PATH = "gateways.json"
    GATEWAYS_KEY = "gateways"
    CARRIER_KEY = "carrier"
    SMS_KEY = "sms"
    MMS_KEY = "mms"
    DEFAULT_TO_MMS = False
    REGION_KEY = "region"
    DEFAULT_REGION = "US"
    SUBJECT_KEY = "subject"
    DEFAULT_SUBJECT = None
    YAGMAIL_KEY = "yagmail"
    DEFAULT_YAGMAIL_ARGS = []


    def __init__(self, number, carrier, username, password, contents=None, **kwargs):
        self.static = MailToSMS

        self.config = {
            "region": kwargs.get(self.static.REGION_KEY, self.static.DEFAULT_REGION),
            "subject": kwargs.get(self.static.SUBJECT_KEY, self.static.DEFAULT_SUBJECT),
            "mms": kwargs.get(self.static.MMS_KEY, self.static.DEFAULT_TO_MMS),
            "yagmail": kwargs.get(self.static.YAGMAIL_KEY, self.static.DEFAULT_YAGMAIL_ARGS)
        }

        ## Prepare the address to send to, return if it couldn't be generated
        self.address = self._build_address(number, carrier)
        if(not self.address):
            return

        ## Prepare the passthru args for yagmail
        yagmail_args = self.config["yagmail"]

        ## Init the yagmail connection
        try:
            self.connection = yagmail.SMTP(username, password, *yagmail_args)
        except Exception as e:
            ## You might want to look into using an app password for this.
            print("Unhandled error creating yagmail connection.", e)
            return

        ## Send the mail if the contents arg has been provided, otherwise
        ## the send() method can be called manually.
        if(contents):
            self.send(contents)


    def _load_gateways(self):
        with open(self.static.GATEWAYS_JSON_PATH, "r") as fd:
            try:
                return json.load(fd)[self.static.GATEWAYS_KEY]
            except Exception as e:
                print("Unhandled error loading gateways.json.", e)
                return []


    def _validate_number(self, number, region):
        try:
            parsed = phonenumbers.parse(number, region)
        except phonenumbers.phonenumberutil.NumberParseException as e:
            print("NumberParseException when parsing the phone number.", e)
            return False
        except Exception as e:
            print("Unhandled error when parsing the phone number.", e)
            return False

        else:
            if (phonenumbers.is_possible_number(parsed) and
                phonenumbers.is_valid_number(parsed)):
                return True
            else:
                print("'{0}' isn't a valid phone number".format(number))
                return False


    def _validate_carrier(self, carrier):
        for gateway in self.gateways:
            if(gateway[self.static.CARRIER_KEY] == carrier):
                return True
        else:
            print("'{0}' isn't a valid carrier.".format(carrier))
            return False


    def _get_gateway(self, carrier):
        for gateway in self.gateways:
            if(gateway[self.static.CARRIER_KEY] == carrier):
                if(self.config.get("mms")):
                    ## Return mms gateway if possible, else return the sms gateway
                    if(self.static.MMS_KEY in gateway):
                        return gateway[self.static.MMS_KEY]
                    elif(self.static.SMS_KEY in gateway):
                        return gateway[self.static.SMS_KEY]
                else:
                    ## Return sms gateway if possible, else return the mms gateway
                    if(self.static.SMS_KEY in gateway):
                        return gateway[self.static.SMS_KEY]
                    elif(self.static.MMS_KEY in gateway):
                        return gateway[self.static.MMS_KEY]
        else:
            ## This shouldn't happen.
            print("Carrier '{0}' doesn't have any valid SMS or MMS gateways.".format(carrier))
            return None


    def _build_address(self, number, carrier):
        ## Parse the phone number and carrier args into strings
        number = str(number).strip()
        carrier = str(carrier).strip()

        ## Load and ensure that there are gateways to check
        self.gateways = self._load_gateways()
        if(not self.gateways):
            return None

        ## Validate the phone number and carrier
        if (not self._validate_number(number, self.config["region"]) or
            not self._validate_carrier(carrier)):
            return None

        ## Get the SMS/MMS gateway for the carrier
        gateway = self._get_gateway(carrier)
        if(not gateway):
            return None

        return "{0}@{1}".format(number, gateway)


    def send(self, contents):
        ## Prepare kwargs for yagmail.send()
        yagmail_kwargs = {
            "to": self.address,
            "subject": self.config["subject"],
            "contents": contents
        }

        ## Send the mail
        try:
            self.connection.send(**yagmail_kwargs)
        except Exception as e:
            print("Unhandled error sending mail.", e)
            return
