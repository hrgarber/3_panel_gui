document.addEventListener('DOMContentLoaded', function() {
    // Chat functionality
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    function addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'ai-message');
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            // Simulate AI response
            setTimeout(() => {
                addMessage("I'm an AI assistant. How can I help you?", false);
            }, 1000);
        }
    }

    // Tab switching functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.getAttribute('data-tab');
            
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        });
    });

    // Code editor enhancements
    const codeEditor = document.querySelector('#code-editor pre code');
    const lines = codeEditor.innerHTML.trim().split('\n');
    codeEditor.innerHTML = lines.map((line, index) => 
        `<span class="line-number">${index + 1}</span>${line}`
    ).join('\n');

    // Browser tab content
    document.getElementById('browser').innerHTML = `
        <div style="padding: 20px; background-color: #fff; color: #000;">
            <h1>Welcome to the Experimental Browser</h1>
            <p>This is a placeholder for browser content.</p>
        </div>
    `;

    // Jupyter IPython tab content
    document.getElementById('jupyter').innerHTML = `
        <div style="padding: 20px;">
            <h2>Jupyter IPython Notebook</h2>
            <pre><code>
# Sample Python code
import pandas as pd
import matplotlib.pyplot as plt

# Create a sample dataframe
df = pd.DataFrame({
    'x': range(1, 11),
    'y': [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
})

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df['x'], df['y'], marker='o')
plt.title('Sample Plot')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.grid(True)
plt.show()
            </code></pre>
        </div>
    `;

    // Terminal simulation
    const terminalContainer = document.getElementById('terminal-container');
    let commandHistory = [];
    let historyIndex = -1;

    function addTerminalLine(content, isCommand = false) {
        const line = document.createElement('div');
        line.innerHTML = isCommand ? `<span class="prompt">&gt;</span> ${content}` : content;
        terminalContainer.insertBefore(line, terminalContainer.lastElementChild);
        terminalContainer.scrollTop = terminalContainer.scrollHeight;
    }

    terminalContainer.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const command = this.textContent.split('> ').pop().trim();
            if (command) {
                addTerminalLine(command, true);
                commandHistory.push(command);
                historyIndex = commandHistory.length;
                executeCommand(command);
            }
            this.textContent = '> ';
            e.preventDefault();
        } else if (e.key === 'ArrowUp') {
            if (historyIndex > 0) {
                historyIndex--;
                this.textContent = `> ${commandHistory[historyIndex]}`;
            }
            e.preventDefault();
        } else if (e.key === 'ArrowDown') {
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                this.textContent = `> ${commandHistory[historyIndex]}`;
            } else {
                historyIndex = commandHistory.length;
                this.textContent = '> ';
            }
            e.preventDefault();
        }
    });

    function executeCommand(command) {
        switch (command.toLowerCase()) {
            case 'help':
                addTerminalLine('Available commands: help, clear, echo, date');
                break;
            case 'clear':
                terminalContainer.innerHTML = '<span class="prompt">&gt;</span> <span class="cursor"></span>';
                break;
            case 'date':
                addTerminalLine(new Date().toString());
                break;
            default:
                if (command.startsWith('echo ')) {
                    addTerminalLine(command.slice(5));
                } else {
                    addTerminalLine(`Command not found: ${command}`);
                }
        }
    }

    // Initial terminal prompt
    terminalContainer.innerHTML = '<span class="prompt">&gt;</span> <span class="cursor"></span>';

    // Make terminal container focusable and focus it
    terminalContainer.setAttribute('tabindex', '0');
    terminalContainer.focus();
});