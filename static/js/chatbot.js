document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById('agro-chat-box');
    const inputField = document.getElementById('agro-input');
    const sendBtn = document.getElementById('agro-send-btn');
    const historyList = document.getElementById('history-list');
    const langSelect = document.getElementById('agro-lang');

    // --- 1. LOAD HISTORY ON START ---
    function loadHistory() {
        const history = JSON.parse(localStorage.getItem('agro_chat_history')) || [];
        chatBox.innerHTML = ''; // Clear current screen
        
        if (history.length === 0) {
            addMessage("Namaste! I am your AgroBot. How can I help you today?", 'bot', false);
        } else {
            history.forEach(msg => {
                addMessage(msg.text, msg.role, false);
            });
        }
        updateHistorySidebar(history);
    }

    // --- 2. SAVE MESSAGE TO HISTORY ---
    function saveToLocalStorage(text, role) {
        const history = JSON.parse(localStorage.getItem('agro_chat_history')) || [];
        history.push({ text, role });
        localStorage.setItem('agro_chat_history', JSON.stringify(history));
        updateHistorySidebar(history);
    }

    // --- 3. UPDATE SIDEBAR (Left Panel) ---
    function updateHistorySidebar(history) {
        historyList.innerHTML = '';
        const userQueries = history.filter(m => m.role === 'user').slice(-5).reverse();
        userQueries.forEach(q => {
            const div = document.createElement('div');
            div.className = 'history-item shadow-sm p-2 mb-2 bg-light rounded small';
            div.innerHTML = `<i class="bi bi-clock-history"></i> ${q.text.substring(0, 20)}...`;
            historyList.appendChild(div);
        });
    }

    // --- 4. SEND MESSAGE LOGIC ---
    async function handleSend() {
        const text = inputField.value.trim();
        if (!text) return;

        addMessage(text, 'user', true); // Add and Save
        inputField.value = '';

        try {
            const res = await fetch('/api/chat/ask', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, lang: langSelect.value })
            });

            const data = await res.json();
            const reply = data.response || data.reply;
            
            addMessage(reply, 'bot', true); // Add and Save

        } catch (e) {
            addMessage("I'm having trouble connecting to the server.", 'bot', false);
        }
    }

    function addMessage(text, role, shouldSave) {
        const div = document.createElement('div');
        div.className = role === 'user' ? 'msg-user shadow-sm' : 'msg-bot shadow-sm';
        div.innerText = text;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;

        if (shouldSave) {
            saveToLocalStorage(text, role);
        }
    }

    // --- 5. VOICE RECOGNITION LOGIC ---
    const micBtn = document.getElementById('agro-mic-btn');
    const micIcon = document.getElementById('mic-icon');
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        micBtn.onclick = () => {
            recognition.lang = langSelect.value; 
            recognition.start();
            micIcon.classList.replace('bi-mic-fill', 'bi-record-circle-fill');
            micIcon.style.color = 'red';
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            inputField.value = transcript; 
            handleSend(); 
        };

        recognition.onend = () => {
            micIcon.classList.replace('bi-record-circle-fill', 'bi-mic-fill');
            micIcon.style.color = '';
        };

        recognition.onerror = (err) => {
            console.error("Speech Error:", err.error);
            micIcon.classList.replace('bi-record-circle-fill', 'bi-mic-fill');
        };
    } else {
        micBtn.style.display = 'none';
    }

    // --- 6. FILE UPLOAD LOGIC ---
    const fileInput = document.getElementById('agro-file-input');

    fileInput.onchange = async () => {
        const file = fileInput.files[0];
        if (!file) return;

        addMessage(`Sending file: ${file.name}`, 'user', true);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('lang', langSelect.value);

        try {
            const res = await fetch('/api/chat/upload', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            addMessage(data.response || "File received!", 'bot', true);
        } catch (e) {
            addMessage("Error uploading file.", 'bot', false);
        }
        fileInput.value = ''; 
    };

    // Event Listeners for original buttons
    sendBtn.onclick = handleSend;
    inputField.onkeypress = (e) => { if(e.key === 'Enter') handleSend(); };
    
    // Initialize
    loadHistory();
});