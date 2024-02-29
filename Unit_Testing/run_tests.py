import unittest
import xmlrunner
import os
import sys


# Import your test cases
import unit_testing
from unit_testing.test_chooser import Testchooser
from unit_testing.test_DicomParser import TestDicomParser
from unit_testing.test_NuSpecGenerator import TestNuspecGenerator
from unit_testing.test_PackageHandler import TestPackageHandler
from unit_testing.test_TDM import TestCLI
# Import other test classes as needed

if __name__ == '__main__':
    # Define the test suite
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()

    # Add test cases from each test class
    test_suite.addTest(test_loader.loadTestsFromTestCase(Testchooser))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestDicomParser))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestNuspecGenerator))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestPackageHandler))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestCLI))
    # Add other test classes as needed

    # Define the test runner with XML output
    output_dir = 'test-reports'
    os.makedirs(output_dir, exist_ok=True)
    test_runner = xmlrunner.XMLTestRunner(output=output_dir)

    # Run the test suite
    test_runner.run(test_suite)
