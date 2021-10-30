import unittest
from mail_to_sms import MailToSMS


class TestMailToSMS(unittest.TestCase):
    def setUp(self):
        self.connection = MailToSMS(None, None, None, None, quiet=True)


    def test_print_error(self):
        testTuples = [
            ## Output producing inputs
            (Exception("test"), "", "test"),
            (Exception("test"), "test message", "test test message"),
            (None, "test message", "test message"),
            (Exception("test"), 12345, "test 12345"),
            (None, True, "True"),
            ## Non-production inputs
            ("", "", None),
            (None, None, None),
            (None, "", None)
        ]

        for exception, message, result in testTuples:
            try:
                self.assertEqual(self.connection._print_error(exception, message), result)
            except AssertionError as e:
                ## Catch the error and dump some useful info, then re-raise it so that the test fails properly
                print("AssertionError: {0} for args: {1}, {2}, {3}".format(e, exception, message, result))
                raise AssertionError(e)


    def test_load_gateways(self):
        pass


    def test_validate_number(self):
        ## Essentially a phonenumbers wrapper, so nothing too extreme for testing
        testTuples = [
            ## (Phone number, Region, Expected Return, Description)
            ## Good inputs
            ("8663454897", "US", True, "US int, US region"),
            (8663454897, "US", True, "US str, US region"),
            ("866 345 4897", "US", True, "US spaced str, US region"),
            ("866-345-4897", "US", True, "US dashed str, US region"),
            ("+1 866 345 4897", None, True, "US international str, None Region"),
            ## Bad inputs
            ("8663454897", None, False, "US str, None region"),
            (8663454897, "GB", False, "US int, GB region"),
            ("abcdefghij", None, False, "alphas str, None region")
        ]

        for number, region, result, description in testTuples:
            try:
                self.assertEqual(self.connection._validate_number(number, region), result)
            except AssertionError as e:
                ## Catch the error and dump some useful info, then re-raise it so that the test fails properly
                print("AssertionError: {0} for args: {1}, {2}, {3}. Description: {4}".format(e, number, region, result, description))
                raise AssertionError(e)


    def test_validate_carrier(self):
        testTuples = [
            ## Good inputs
            ("alltel", True),
            ("at&t", True),
            ("att", True),
            ("boost mobile", True),
            ("boost", True),
            ("cricket wireless", True),
            ("cricket", True),
            ("metropcs", True),
            ("project fi", True),
            ("fi", True),
            ("sprint", True),
            ("t-mobile", True),
            ("tmobile", True),
            ("us cellular", True),
            ("verizon wireless", True),
            ("verizon", True),
            ("vzw", True),
            ("virgin mobile", True),
            ("virgin", True),
            ## Bad inputs
            (None, False),
            (12345, False),
            ("", False),
            (" ", False),
            ("12345", False),
            ("at t", False),
        ]

        for carrier, result in testTuples:
            try:
                self.assertEqual(self.connection._validate_carrier(carrier), result)
            except AssertionError as e:
                ## Catch the error and dump some useful info, then re-raise it so that the test fails properly
                print("AssertionError: {0} for args: {1}, {2}.".format(e, carrier, result))
                raise AssertionError(e)


    def test_get_gateway(self):
        def do_test(testDicts):
            mms = self.connection.config["mms"]

            for trial in testDicts:
                try:
                    if(mms):
                        result = trial["mms"]
                    else:
                        result = trial["sms"]

                    self.assertEqual(self.connection._get_gateway(trial["carrier"]), result)
                except AssertionError as e:
                    ## Catch the error and dump some useful info, then re-raise it so that the test fails properly
                    print("AssertionError: {0} for args: {1}, {2}.".format(e, trial["carrier"], result))
                    raise AssertionError(e)

        testDicts = [
            ## Good inputs
            {"carrier":"att", "sms":"txt.att.net", "mms":"mms.att.net"},
            {"carrier":"sprint", "sms":"messaging.sprintpcs.com", "mms":"pm.sprint.com"},
            ## Bad inputs
            {"carrier":12345, "sms":None, "mms":None},
            {"carrier":"", "sms":None, "mms":None},
            {"carrier":"not a carrier", "sms":None, "mms":None},
        ]

        ## Test without any config kwargs
        do_test(testDicts)

        ## Test with mms kwarg
        self.connection = MailToSMS(None, None, None, None, mms=True, quiet=True)
        do_test(testDicts)


    def test_build_address(self):
        testTuples = [
            ## Good inputs
            (8663454897, "att", "8663454897@txt.att.net"),
            ("8663454897", "sprint", "8663454897@messaging.sprintpcs.com"),
            ("8663454897", "virgin mobile", "8663454897@vmobl.com"),
            ## Bad inputs
            (None, None, None),
            ("", "att", None),
            ("abcdefg", "sprint", None),
            (8663454897, None, None),
            (8663454897, "not a carrier", None)
        ]

        for number, carrier, result in testTuples:
            try:
                self.assertEqual(self.connection._build_address(number, carrier), result)
            except AssertionError as e:
                ## Catch the error and dump some useful info, then re-raise it so that the test fails properly
                print("AssertionError: {0} for args: {1}, {2}, {3}.".format(e, number, carrier, result))
                raise AssertionError(e)


    def test_send(self):
        pass


if(__name__ == "__main__"):
    unittest.main()