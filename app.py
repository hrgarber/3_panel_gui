import streamlit as st
import streamlit.components.v1 as components
import json

# Initialize session state for in-memory storage
if 'conversations' not in st.session_state:
    st.session_state.conversations = {}
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Mock LLM response function
def get_llm_response(message):
    return f"Echo: {message}"

# Function to handle chat messages
def handle_chat(user_id, message):
    if user_id not in st.session_state.conversations:
        st.session_state.conversations[user_id] = []
    
    st.session_state.conversations[user_id].append({'role': 'user', 'content': message})
    llm_response = get_llm_response(message)
    st.session_state.conversations[user_id].append({'role': 'assistant', 'content': llm_response})
    
    return llm_response

# Function to set user ID
def set_user_id(user_id):
    if user_id not in st.session_state.user_data:
        st.session_state.user_data[user_id] = {'id': user_id}
    return {'status': 'success', 'user_id': user_id}

# Function to get current state as a string
def get_current_state():
    state = {
        'conversations': st.session_state.conversations,
        'user_data': st.session_state.user_data
    }
    return json.dumps(state, indent=2)

# Read HTML, CSS, and JS files with UTF-8 encoding
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

with open('styles.css', 'r', encoding='utf-8') as file:
    css_content = file.read()

with open('script.js', 'r', encoding='utf-8') as file:
    js_content = file.read()

# Streamlit app
st.set_page_config(layout="wide", page_title="3-Panel GUI")

# Function to handle incoming messages from frontend
def handle_frontend_message(message):
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
            # Print the current state to the console
            print("\n--- Current State ---")
            print(current_state)
            print("---------------------\n")
            return json.dumps({'type': 'print_state', 'state': current_state})
    except json.JSONDecodeError:
        st.error("Invalid JSON input")
    return None

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
    st.write("Conversations:", st.session_state.conversations)
    st.write("User data:", st.session_state.user_data)