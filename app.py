import streamlit as st
import streamlit.components.v1 as components
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Streamlit app
st.set_page_config(layout="wide", page_title="3-Panel GUI")

# Initialize session state for conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Load API key from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    response = model.invoke(input_text)
    return response.content

# Read HTML, CSS, and JS files
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

with open('styles.css', 'r', encoding='utf-8') as file:
    css_content = file.read()

with open('script.js', 'r', encoding='utf-8') as file:
    js_content = file.read()

# Inject CSS and JS into HTML
html_with_css_js = html_content.replace('</head>', f'<style>{css_content}</style></head>')
html_with_css_js = html_with_css_js.replace('</body>', f'<script>{js_content}</script></body>')

# Handle chat messages
def handle_chat_message(message):
    st.session_state.messages.append({"role": "user", "content": message})
    response = generate_response(message)
    st.session_state.messages.append({"role": "assistant", "content": response})
    return response

# Callback for handling frontend messages
def handle_frontend_message():
    if st.session_state.frontend_input:
        try:
            data = json.loads(st.session_state.frontend_input)
            if data['type'] == 'chat':
                response = handle_chat_message(data['message'])
                # Send the response back to the frontend
                st.components.v1.html(
                    f"""
                    <script>
                    window.parent.postMessage({{
                        type: "streamlit:render",
                        args: {{ data: {json.dumps({'type': 'chat', 'response': response})} }}
                    }}, "*");
                    </script>
                    """,
                    height=0,
                    width=0,
                )
        except json.JSONDecodeError:
            st.error("Invalid JSON input")
        st.session_state.frontend_input = ''  # Clear the input after processing

# Create a hidden text input for frontend messages
st.text_input("Frontend message", key="frontend_input", on_change=handle_frontend_message, label_visibility="hidden")

# Inject custom HTML/CSS/JS
components.html(html_with_css_js, height=800, scrolling=False)

# Remove all Streamlit elements
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp header {visibility: hidden;}
    .stTextInput {visibility: hidden;}
    .stButton {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Display current state (for debugging)
if st.checkbox("Show conversation history"):
    st.write("Conversation History:", st.session_state.messages)
