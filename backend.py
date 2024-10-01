from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage
conversations = {}
user_data = {}

# Mock LLM response function
def get_llm_response(message):
    return f"Echo: {message}"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')
    
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({'role': 'user', 'content': message})
    
    llm_response = get_llm_response(message)
    
    conversations[user_id].append({'role': 'assistant', 'content': llm_response})
    
    return jsonify({'response': llm_response})

@app.route('/api/set_user_id', methods=['POST'])
def set_user_id():
    data = request.json
    user_id = data.get('user_id')
    
    if user_id not in user_data:
        user_data[user_id] = {'id': user_id}
    
    return jsonify({'status': 'success'})

# This function will be called from the Streamlit app to run the Flask app
def run_flask():
    app.run(port=5000, debug=True, use_reloader=False)