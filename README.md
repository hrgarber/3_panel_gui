# 3-Panel GUI

This project is a Streamlit-powered chat interface with a 3-panel GUI layout. It features a chat panel, a code editor, and a terminal simulation, all integrated with a Streamlit backend for robust in-memory persistence and seamless interaction between the frontend and backend.

## Features

- **Chat Interface**: Allows users to interact with an AI assistant (currently using a mock LLM response).
- **Code Editor**: Provides a syntax-highlighted Python code editor.
- **Terminal Simulation**: Offers a basic terminal-like interface for executing simple commands.
- **User ID System**: Supports multiple users with unique conversation histories.
- **In-Memory Persistence**: Utilizes Streamlit's session state for storing conversation and user data.
- **Responsive Design**: Features a clean, modern interface with a dark theme.

## Technologies Used

- **Backend**: Streamlit
- **Frontend**: HTML, CSS, JavaScript
- **Syntax Highlighting**: Prism.js

## Setup and Running the Application

1. Ensure you have Python 3.7+ installed on your system.

2. Install the required dependencies:
   ```
   pip install streamlit
   ```

3. Clone this repository and navigate to the project directory:
   ```
   git clone https://github.com/yourusername/3_panel_gui.git
   cd 3_panel_gui
   ```

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

5. Open your web browser and go to the URL provided by Streamlit (usually http://localhost:8501).

## Usage

1. When you first open the application, you'll be prompted to set a User ID. This ID is used to manage your conversation history.

2. Use the chat interface in the left panel to interact with the AI assistant.

3. The top-right panel contains a code editor where you can write and edit Python code. The syntax is automatically highlighted.

4. The bottom-right panel simulates a terminal. You can use commands like `help`, `clear`, `echo`, `date`, `userid`, and `printstate`.

5. You can switch between different tabs in the top-right panel, although only the code editor is currently functional.

## Project Structure

- `app.py`: The main Streamlit application file containing the backend logic and in-memory persistence system.
- `index.html`: The HTML structure of the 3-panel GUI.
- `styles.css`: CSS styles for the application.
- `script.js`: JavaScript code for frontend interactivity and communication with the Streamlit backend.

## Future Improvements

- Implement a real Language Model for more sophisticated AI responses.
- Add functionality to the Browser and Jupyter IPython tabs.
- Enhance the terminal simulation with more advanced features.
- Implement persistent storage for user data and conversations.

## Contributing

Contributions to improve the application are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).