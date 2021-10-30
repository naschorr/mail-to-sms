import sys
import os.path
import inspect
import unittest
import pkgutil
import importlib
from pathlib import Path
from unittest.runner import TextTestResult

## Based on: https://github.com/naschorr/electronic-component-label-builder/blob/master/testing/testRunner.py

## Assumes this file is at /<root>/tests/test_runner.py
## Then, it just adds the /<root>/mail_to_sms/ directory to the PYTHONPATH so the tests can be run
# sys.path.append(os.path.sep.join(os.path.realpath(__file__).split(os.path.sep)[:-2] + ["mail_to_sms"]))
sys.path.append(os.path.sep.join(os.path.realpath(__file__).split(os.path.sep)[:-2] + ["tests"]))

import tests

def discover_test_cases(root_module):
	test_cases = []

	module_info: pkgutil.ModuleInfo
	for module_info in [info for info in pkgutil.iter_modules([root_module.__path__._path[0]])]:
		## Ignore this file, obviously it doesn't have any test cases
		if (module_info.module_finder.path == __file__):
			continue

		sys.path.append(Path(module_info.module_finder.path)/module_info.name)
		module = importlib.import_module(module_info.name)

		for _, cls in inspect.getmembers(module, inspect.isclass):
			if(unittest.TestCase.__name__ in [base.__name__ for base in cls.__bases__] and module.__name__ != unittest.__name__):
				test_cases.append(cls)

	if(not test_cases):
		print("Didn't find any test cases. Are they in the correct directory, and are they built with Python's unittest module?")

	return test_cases


def build_test_suite(test_cases):
	suite = unittest.TestSuite()
	for testCase in test_cases:
		suite.addTest(unittest.makeSuite(testCase))

	return suite


def main() -> bool:
	runner = unittest.TextTestRunner()

	try:
		test_cases = discover_test_cases(tests)
		test_suite = build_test_suite(test_cases)
		results: TextTestResult = runner.run(test_suite)
		success = results.wasSuccessful()
	except:
		success = False

	return success


if __name__ == "__main__":
	main()