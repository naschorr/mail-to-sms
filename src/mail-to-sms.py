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
    """
        MailToSMS Docstring
    """

    ## Config
    GATEWAYS_JSON_PATH = "gateways.json"
    GATEWAYS_KEY = "gateways"
    CARRIER_KEY = "carrier"
    SMS_KEY = "sms"
    MMS_KEY = "mms"


    def __init__(self, number, carrier, username, password, contents, **kwargs):
        self.static = MailToSMS

        self.gateways = self.load_gateways()
        if(not self.gateways):
            return

        number = self.validate_number(number, kwargs.get("region", "US"))
        carrier = self.validate_carrier(carrier)
        if(not number or not carrier):
            return

        gateway = self.get_gateway(carrier)
        if(not gateway):
            return

        ## Prepare kwargs for yagmail
        yagmail_kwargs = {}
        yagmail_kwargs["to"] = "{0}@{1}".format(number, gateway)
        if(kwargs.get("subject", False)):
            yagmail_kwargs["subject"] = kwargs["subject"]
        yagmail_kwargs["contents"] = contents

        ## Init the yagmail connection
        try:
            connection = yagmail.SMTP(username, password)
        except Exception as e:
            ## You might want to look into using an app password for this.
            print("Unhandled error creating yagmail connection.\nSee the following error text:", e)
            return

        ## Send the mail
        try:
            connection.send(**yagmail_kwargs)
        except Exception as e:
            print("Unhandled error creating sending mail", e)
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
        else:
            print("{0} doesn't have any valid gateways.".format(carrier))   # This shouldn't happen.
            return ""
