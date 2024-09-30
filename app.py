import streamlit as st
import streamlit.components.v1 as components

# Read HTML, CSS, and JS files with UTF-8 encoding
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

with open('styles.css', 'r', encoding='utf-8') as file:
    css_content = file.read()

with open('script.js', 'r', encoding='utf-8') as file:
    js_content = file.read()

# Streamlit app
st.set_page_config(layout="wide", page_title="3-Panel GUI")

# Inject CSS and JS into HTML
html_with_css_js = html_content.replace('</head>', f'<style>{css_content}</style></head>')
html_with_css_js = html_with_css_js.replace('</body>', f'<script>{js_content}</script></body>')

# Inject custom HTML/CSS/JS
st.components.v1.html(html_with_css_js, height=1000, scrolling=False)

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