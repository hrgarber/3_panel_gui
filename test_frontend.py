import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import subprocess
import requests

class TestChatFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start Streamlit app if it's not already running
        cls.streamlit_process = None
        try:
            requests.get("http://localhost:8501")
        except requests.ConnectionError:
            print("Starting Streamlit app...")
            cls.streamlit_process = subprocess.Popen(["streamlit", "run", "app.py"])
            time.sleep(15)  # Wait longer for Streamlit to start

    @classmethod
    def tearDownClass(cls):
        if cls.streamlit_process:
            cls.streamlit_process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8501")
        time.sleep(15)  # Wait longer for the page to load

    def tearDown(self):
        self.driver.quit()

    def test_send_message(self):
        try:
            # Wait for the iframe to be present
            iframe = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            
            # Switch to the iframe
            self.driver.switch_to.frame(iframe)
            
            # Wait for the input field to be present and interactable
            input_field = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Type a message...']"))
            )
            
            # Type a message
            input_field.clear()
            input_field.send_keys("Test message")
            
            # Find and click the send button
            send_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#send-button"))
            )
            send_button.click()
            
            # Wait for the user message to appear
            WebDriverWait(self.driver, 30).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "user-message"), "Test message")
            )
            
            # Wait for the AI response
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ai-message"))
            )
            
            # Check if the message was sent and a response was received
            messages = self.driver.find_elements(By.CLASS_NAME, "message")
            self.assertGreaterEqual(len(messages), 2)  # At least user message and AI response
            self.assertEqual(messages[-2].text, "Test message")
            self.assertIsNotNone(messages[-1].text)
            
        except TimeoutException as e:
            self.fail(f"Timed out waiting for page elements: {str(e)}")
        except Exception as e:
            self.fail(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    unittest.main()