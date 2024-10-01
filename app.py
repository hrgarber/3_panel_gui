import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, List
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up Langchain ChatOpenAI model
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))

class Conversation:
    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages

class UserData:
    def __init__(self, user_id: str):
        self.id = user_id

class AppState:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        self.user_data: Dict[str, UserData] = {}

    def get_or_create_conversation(self, user_id: str) -> Conversation:
        if user_id not in self.conversations:
            self.conversations[user_id] = Conversation()
        return self.conversations[user_id]

    def set_user_data(self, user_id: str):
        if user_id not in self.user_data:
            self.user_data[user_id] = UserData(user_id)

    def to_dict(self) -> Dict:
        return {
            "conversations": {user_id: conv.get_messages() for user_id, conv in self.conversations.items()},
            "user_data": {user_id: {"id": user.id} for user_id, user in self.user_data.items()}
        }

# Initialize session state
if 'app_state' not in st.session_state:
    st.session_state.app_state = AppState()

def get_llm_response(messages: List[Dict[str, str]]) -> str:
    try:
        langchain_messages = [
            SystemMessage(content="You are a helpful assistant."),
            *[HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"])
              for msg in messages[1:]]  # Skip the first system message
        ]
        response = llm(langchain_messages)
        return response.content
    except Exception as e:
        st.error(f"Error in LLM response: {str(e)}")
        return "I'm sorry, but I encountered an error. Please try again."

def handle_chat(user_id: str, message: str) -> str:
    conversation = st.session_state.app_state.get_or_create_conversation(user_id)
    conversation.add_message("user", message)
    
    llm_response = get_llm_response(conversation.get_messages())
    conversation.add_message("assistant", llm_response)
    return llm_response

def set_user_id(user_id: str) -> Dict[str, str]:
    st.session_state.app_state.set_user_data(user_id)
    return {"status": "success", "user_id": user_id}

def get_current_state() -> str:
    return json.dumps(st.session_state.app_state.to_dict(), indent=2)

def handle_frontend_message(message: str) -> str:
    try:
        data = json.loads(message)
        if data['type'] == 'chat':
            response = handle_chat(data['user_id'], data['message'])
            return json.dumps({'type': 'chat', 'response': response})
        elif data['type'] == 'set_user_id':
            response = set_user_id(data['user_id'])
            return json.dumps({'type': 'set_user_id', 'user_id': response['user_id']})
        elif data['type'] == 'print_state':
            current_state = get_current_state()
            print("\n--- Current State ---")
            print(current_state)
            print("---------------------\n")
            return json.dumps({'type': 'print_state', 'state': current_state})
    except json.JSONDecodeError:
        st.error("Invalid JSON input")
    return ""

# Streamlit app
st.set_page_config(layout="wide", page_title="3-Panel GUI")

# Read HTML, CSS, and JS files
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

with open('styles.css', 'r', encoding='utf-8') as file:
    css_content = file.read()

with open('script.js', 'r', encoding='utf-8') as file:
    js_content = file.read()

# Create a placeholder for frontend messages
frontend_message = st.empty()

# Handle frontend messages
if frontend_message.text_input("Frontend message"):
    response = handle_frontend_message(frontend_message.text_input("Frontend message"))
    if response:
        st.write(f"Response: {response}")
        # Send the response back to the frontend
        st.components.v1.html(
            f"""
            <script>
            window.parent.postMessage({{
                type: "streamlit:message",
                data: {json.dumps(response)}
            }}, "*");
            </script>
            """,
            height=0,
            width=0,
        )

# Inject CSS and JS into HTML
html_with_css_js = html_content.replace('</head>', f'<style>{css_content}</style></head>')
html_with_css_js = html_with_css_js.replace('</body>', f'<script>{js_content}</script></body>')

# Inject custom HTML/CSS/JS
components.html(html_with_css_js, height=1000, scrolling=False)

# Remove all Streamlit elements
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Display current state (for debugging)
if st.checkbox("Show current state"):
    st.write("Current State:", st.session_state.app_state.to_dict())
