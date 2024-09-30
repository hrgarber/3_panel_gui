import streamlit as st
import streamlit.components.v1 as components

# Read CSS and JS files with UTF-8 encoding
with open('styles.css', 'r', encoding='utf-8') as file:
    css_content = file.read()

with open('script.js', 'r', encoding='utf-8') as file:
    js_content = file.read()

# Streamlit app
st.set_page_config(layout="wide", page_title="3-Panel GUI")

# Add a title to check if Streamlit is rendering correctly
st.title("3-Panel GUI")

# Custom HTML structure
custom_html = """
<div class="container">
    <header class="top-bar">
        <div class="menu-items">
            <button class="menu-item">File</button>
            <button class="menu-item">Edit</button>
            <button class="menu-item">View</button>
        </div>
    </header>
    <div class="main-content">
        <div class="panel chat-panel">
            <div class="panel-label">Panel 1</div>
            <div class="panel-content">
                <div class="chat-messages" id="chat-messages">
                    <!-- Chat messages will be dynamically added here -->
                </div>
                <div class="chat-input">
                    <input type="text" id="user-input" placeholder="Type a message...">
                    <button id="send-button">Send</button>
                </div>
            </div>
        </div>
        <div class="right-panels">
            <div class="panel top-right-panel">
                <div class="panel-label">Panel 2</div>
                <div class="panel-content">
                    <div class="tabs">
                        <button class="tab-button active" data-tab="code-editor">Editor</button>
                        <button class="tab-button" data-tab="browser">Browser (Experimental)</button>
                        <button class="tab-button" data-tab="jupyter">Jupyter IPython</button>
                    </div>
                    <div class="tab-content active" id="code-editor">
                        <div class="editor-header">
                            <span>Workspace</span>
                            <div class="editor-actions">
                                <button class="editor-action">↻</button>
                                <button class="editor-action">☁</button>
                                <button class="editor-action">&lt;</button>
                            </div>
                        </div>
                        <div class="editor-content">
                            <div class="line-numbers"></div>
                            <pre><code class="language-python" id="code-area">
def hello_world():
    print("Hello, World!")

hello_world()
</code></pre>
                        </div>
                    </div>
                    <div class="tab-content" id="browser">
                        <h2>Browser (Experimental)</h2>
                        <p>No file selected.</p>
                    </div>
                    <div class="tab-content" id="jupyter">
                        <h2>Jupyter IPython</h2>
                        <p>No file selected.</p>
                    </div>
                </div>
            </div>
            <div class="panel terminal-panel">
                <div class="panel-label">Panel 3</div>
                <div class="panel-content">
                    <div class="terminal-header">Terminal</div>
                    <div id="terminal-container">
                        <span class="prompt">$</span>
                        <span class="cursor"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <footer class="status-bar">
        <span>Agent is initialized, waiting for task...</span>
    </footer>
</div>
"""

# Additional CSS to adjust layout and styling
additional_css = """
<style>
body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    font-family: Arial, sans-serif;
}
.stApp {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: hidden;
}
.main .block-container {
    max-width: 100% !important;
    padding-top: 0 !important;
    padding-right: 0 !important;
    padding-left: 0 !important;
    padding-bottom: 0 !important;
}
.container {
    height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #1e1e1e;
    color: #d4d4d4;
}
.top-bar, .status-bar {
    background-color: #2d2d2d;
    padding: 5px 10px;
}
.main-content {
    display: flex;
    flex: 1;
    overflow: hidden;
}
.chat-panel {
    width: 30%;
    border-right: 1px solid #3d3d3d;
    background-color: #252526;
}
.right-panels {
    display: flex;
    flex-direction: column;
    width: 70%;
}
.top-right-panel {
    height: 60%;
    border-bottom: 1px solid #3d3d3d;
    background-color: #1e1e1e;
}
.terminal-panel {
    height: 40%;
    background-color: #1e1e1e;
}
.panel-content {
    height: 100%;
    overflow: auto;
    padding: 10px;
}
.panel-label {
    background-color: rgba(0, 0, 0, 0.3);
    padding: 2px 5px;
    position: absolute;
    top: 5px;
    left: 5px;
    font-size: 12px;
}
.chat-messages {
    height: calc(100% - 40px);
    overflow-y: auto;
}
.chat-input {
    display: flex;
    padding: 5px;
    background-color: #2d2d2d;
}
.chat-input input {
    flex: 1;
    margin-right: 5px;
    background-color: #3c3c3c;
    border: none;
    color: #d4d4d4;
    padding: 5px;
}
.chat-input button, .menu-item, .tab-button, .editor-action {
    background-color: #0e639c;
    border: none;
    color: #ffffff;
    padding: 5px 10px;
    cursor: pointer;
}
.editor-content {
    display: flex;
    height: calc(100% - 60px);
}
.line-numbers {
    padding: 10px 5px;
    background-color: #1e1e1e;
    color: #858585;
    text-align: right;
    user-select: none;
}
#code-area {
    flex: 1;
    margin: 0;
    padding: 10px;
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.5;
    overflow: auto;
}
#terminal-container {
    height: calc(100% - 30px);
    padding: 10px;
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.5;
    overflow: auto;
}
.prompt {
    color: #569cd6;
}
.cursor {
    display: inline-block;
    width: 8px;
    height: 15px;
    background-color: #d4d4d4;
    animation: blink 1s step-end infinite;
}
@keyframes blink {
    50% { opacity: 0; }
}
</style>
"""

# Combine HTML, CSS, and JS
combined_content = f"""
<style>
{css_content}
</style>
{additional_css}
{custom_html}
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-python.min.js"></script>
<script>
{js_content}
</script>
"""

# Print the combined_content to check if it's being generated correctly
print("Combined content generated successfully. Length:", len(combined_content))

# Inject custom HTML/CSS/JS
st.components.v1.html(combined_content, height=1000, scrolling=False)

# Remove all Streamlit elements
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)