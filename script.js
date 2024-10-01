document.addEventListener('DOMContentLoaded', function() {
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
            sendToBackend('chat', { message: message });
        }
    }

    function sendToBackend(type, data) {
        const message = JSON.stringify({ type, ...data });
        window.parent.postMessage({
            type: "streamlit:setComponentValue",
            value: message
        }, "*");
    }

    window.addEventListener("message", function(event) {
        if (event.data.type === "streamlit:render") {
            const data = JSON.parse(event.data.args.data);
            if (data.type === "chat") {
                addMessage(data.response, false);
            }
        }
    });

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
    const codeArea = document.getElementById('code-area');
    const lineNumbers = document.querySelector('.line-numbers');

    function updateLineNumbers() {
        const lines = codeArea.textContent.split('\n');
        lineNumbers.innerHTML = lines.map((_, index) => `<div>${index + 1}</div>`).join('');
    }

    function updateCode() {
        const code = codeArea.textContent;
        codeArea.innerHTML = Prism.highlight(code, Prism.languages.python, 'python');
        updateLineNumbers();
    }

    codeArea.addEventListener('input', updateCode);
    codeArea.addEventListener('scroll', () => {
        lineNumbers.scrollTop = codeArea.scrollTop;
    });

    // Initial code update
    updateCode();

    // Make code area editable
    codeArea.setAttribute('contenteditable', 'true');

    // Terminal simulation
    const terminalContainer = document.getElementById('terminal-container');
    let commandHistory = [];
    let historyIndex = -1;

    function addTerminalLine(content, isCommand = false) {
        const line = document.createElement('div');
        line.innerHTML = isCommand ? `<span class="prompt">$</span> ${content}` : content;
        terminalContainer.insertBefore(line, terminalContainer.lastElementChild);
        terminalContainer.scrollTop = terminalContainer.scrollHeight;
    }

    terminalContainer.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const command = this.textContent.split('$ ').pop().trim();
            if (command) {
                addTerminalLine(command, true);
                commandHistory.push(command);
                historyIndex = commandHistory.length;
                executeCommand(command);
            }
            this.innerHTML = '<span class="prompt">$</span> <span class="cursor"></span>';
            e.preventDefault();
        } else if (e.key === 'ArrowUp') {
            if (historyIndex > 0) {
                historyIndex--;
                this.innerHTML = `<span class="prompt">$</span> ${commandHistory[historyIndex]}<span class="cursor"></span>`;
            }
            e.preventDefault();
        } else if (e.key === 'ArrowDown') {
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                this.innerHTML = `<span class="prompt">$</span> ${commandHistory[historyIndex]}<span class="cursor"></span>`;
            } else if (historyIndex === commandHistory.length - 1) {
                historyIndex++;
                this.innerHTML = '<span class="prompt">$</span> <span class="cursor"></span>';
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
                terminalContainer.innerHTML = '<span class="prompt">$</span> <span class="cursor"></span>';
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
    terminalContainer.innerHTML = '<span class="prompt">$</span> <span class="cursor"></span>';

    // Make terminal container focusable and focus it
    terminalContainer.setAttribute('tabindex', '0');
    terminalContainer.focus();
});