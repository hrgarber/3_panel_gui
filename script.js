document.addEventListener('DOMContentLoaded', function() {
    // Chat functionality
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    let currentUserId = null;

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
        if (message && currentUserId) {
            addMessage(message, true);
            userInput.value = '';
            sendToBackend('chat', { user_id: currentUserId, message: message });
        } else if (!currentUserId) {
            addMessage("Please set a User ID first.", false);
        }
    }

    // Function to send data to Streamlit backend
    function sendToBackend(type, data) {
        const message = JSON.stringify({ type, ...data });
        window.parent.postMessage({ type: "streamlit:message", data: message }, "*");
    }

    // Function to receive messages from Streamlit backend
    window.addEventListener("message", function(event) {
        if (event.data.type === "streamlit:render") {
            const data = JSON.parse(event.data.data);
            if (data.type === "chat") {
                addMessage(data.response, false);
            } else if (data.type === "set_user_id") {
                addTerminalLine(`User ID set to: ${data.user_id}`);
            } else if (data.type === "print_state") {
                addTerminalLine("Current State:");
                addTerminalLine(data.state);
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
                addTerminalLine('Available commands: help, clear, echo, date, userid, printstate');
                break;
            case 'clear':
                terminalContainer.innerHTML = '<span class="prompt">$</span> <span class="cursor"></span>';
                break;
            case 'date':
                addTerminalLine(new Date().toString());
                break;
            case 'userid':
                if (currentUserId) {
                    addTerminalLine(`Current User ID: ${currentUserId}`);
                } else {
                    addTerminalLine('No User ID set. Use the File > User ID option to set one.');
                }
                break;
            case 'printstate':
                sendToBackend('print_state', {});
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

    // User ID functionality
    const userIdOption = document.getElementById('user-id-option');
    const userIdModal = document.getElementById('user-id-modal');
    const userIdInput = document.getElementById('user-id-input');
    const userIdSubmit = document.getElementById('user-id-submit');

    userIdOption.addEventListener('click', function(e) {
        e.preventDefault();
        userIdModal.style.display = 'block';
    });

    userIdSubmit.addEventListener('click', function() {
        const newUserId = userIdInput.value.trim();
        if (newUserId) {
            currentUserId = newUserId;
            userIdModal.style.display = 'none';
            sendToBackend('set_user_id', { user_id: currentUserId });
        }
    });

    window.addEventListener('click', function(e) {
        if (e.target === userIdModal) {
            userIdModal.style.display = 'none';
        }
    });
});