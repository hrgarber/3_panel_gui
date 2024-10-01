import unittest
import sys
from test_app import TestApp

def run_tests(test_names=None):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if test_names:
        for test_name in test_names:
            try:
                suite.addTest(loader.loadTestsFromName(f'test_app.TestApp.{test_name}'))
            except AttributeError:
                print(f"Warning: Test '{test_name}' not found in TestApp class.")
    else:
        suite.addTest(loader.loadTestsFromTestCase(TestApp))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result

if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_names = sys.argv[1:]
        result = run_tests(test_names)
    else:
        result = run_tests()

    if result.wasSuccessful():
        print("All tests passed successfully!")
    else:
        print("Some tests failed.")
    
    sys.exit(not result.wasSuccessful())