#!/usr/bin/env python3
import unittest
import sys
from test_app import TestApp

def run_unittest_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TestApp))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result

if __name__ == '__main__':
    result = run_unittest_tests()
    
    if result.wasSuccessful():
        print("\nAll backend tests passed successfully!")
    else:
        print("\nSome backend tests failed.")
    
    sys.exit(not result.wasSuccessful())