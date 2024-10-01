import unittest
import test_app
import test_frontend

def run_tests():
    # Create a test suite
    test_suite = unittest.TestSuite()

    # Add the tests from test_app.py
    test_suite.addTest(unittest.makeSuite(test_app.TestApp))

    # Add the tests from test_frontend.py
    test_suite.addTest(unittest.makeSuite(test_frontend.TestChatFunctionality))

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Return the result
    return result

if __name__ == '__main__':
    result = run_tests()
    if result.wasSuccessful():
        print("All tests passed!")
    else:
        print("Some tests failed.")