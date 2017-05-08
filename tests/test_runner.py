import sys
import os.path
import inspect
import unittest

## Based on: https://github.com/naschorr/electronic-component-label-builder/blob/master/testing/testRunner.py

## Assumes this file is at /<root>/tests/test_runner.py
## Then, it just adds the /<root>/src/ directory to the PYTHONPATH so the tests can be run
sys.path.append(os.path.sep.join(os.path.realpath(__file__).split(os.path.sep)[:-2] + ["src"]))

import mail_to_sms_test

def discover_test_cases():
	test_cases = []
	for module_name, module in inspect.getmembers(sys.modules[__name__], inspect.ismodule):
		for clsName, cls in inspect.getmembers(module, inspect.isclass):
			if(unittest.TestCase.__name__ in [base.__name__ for base in cls.__bases__] and module_name != unittest.__name__):
				test_cases.append(cls)
	
	if(not test_cases):
		print("Didn't find any test cases. Are they in the correct directory, and are they built with Python's unittest module?")

	return test_cases


def build_test_suite(test_cases):
	suite = unittest.TestSuite()
	for testCase in test_cases:
		suite.addTest(unittest.makeSuite(testCase))

	return suite


def main():
	runner = unittest.TextTestRunner()
	runner.run(build_test_suite(discover_test_cases()))

if __name__ == "__main__":
	main()