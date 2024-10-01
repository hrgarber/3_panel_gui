import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Add the current directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import app

class TestApp(unittest.TestCase):

    def setUp(self):
        # Mock Streamlit
        self.streamlit_mock = patch('app.st').start()
        
        # Create a MagicMock for session_state
        self.session_state_mock = MagicMock()
        self.session_state_mock.messages = []
        self.session_state_mock.frontend_input = ''
        
        # Assign the MagicMock to st.session_state
        self.streamlit_mock.session_state = self.session_state_mock

        # Mock OpenAI API key
        os.environ['OPENAI_API_KEY'] = 'test_api_key'

    def tearDown(self):
        patch.stopall()

    def test_generate_response(self):
        with patch('app.ChatOpenAI') as mock_chat:
            mock_chat.return_value.invoke.return_value.content = "Test response"
            response = app.generate_response("Test input")
            self.assertEqual(response, "Test response")

    def test_handle_chat_message(self):
        with patch('app.generate_response') as mock_generate:
            mock_generate.return_value = "AI response"
            response = app.handle_chat_message("User message")
            self.assertEqual(response, "AI response")
            self.assertEqual(self.session_state_mock.messages, [
                {"role": "user", "content": "User message"},
                {"role": "assistant", "content": "AI response"}
            ])

    def test_handle_frontend_message_valid_json(self):
        self.session_state_mock.frontend_input = json.dumps({"type": "chat", "message": "Hello"})
        with patch('app.handle_chat_message') as mock_handle:
            mock_handle.return_value = "AI response"
            app.handle_frontend_message()
            mock_handle.assert_called_once_with("Hello")

    def test_handle_frontend_message_invalid_json(self):
        self.session_state_mock.frontend_input = "Invalid JSON"
        with patch('app.st.error') as mock_error:
            app.handle_frontend_message()
            mock_error.assert_called_once_with("Invalid JSON input")

if __name__ == '__main__':
    unittest.main()