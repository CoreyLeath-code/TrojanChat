// ============================================
// TrojanChat — Web Client (WebSocket Version)
// ============================================

const API_HOST = window.location.hostname || "localhost";
const WS_URL = `ws://${API_HOST}:8000/ws/chat`;
const HTTP_URL = `http://${API_HOST}:8000`;

const messagesDiv = document.getElementById("messages");
const messageInput = document.getElementById("message");
const usernameInput = document.getElementById("username");
const sendButton = document.getElementById("sendBtn");

let socket;

function connectWebSocket() {
    socket = new WebSocket(WS_URL);

    socket.onmessage = function (event) {
        const msg = JSON.parse(event.data);
        appendMessage(msg);
    };

    socket.onclose = () => {
        console.warn("WebSocket interface disconnected. Retrying connection context...");
        setTimeout(connectWebSocket, 1000);
    };

    socket.onerror = (err) => {
        console.error("WebSocket socket anomaly tracked:", err);
        socket.close();
    };
}

// Initialize active connection channel
connectWebSocket();

function appendMessage(msg) {
    const div = document.createElement("div");
    div.classList.add("message");

    const rawTime = msg.timestamp || new Date().toISOString();
    const time = rawTime.replace("T", " ").split(".")[0];

    div.innerHTML = `
        <div class="message-username">${msg.username}</div>
        <div class="message-text">${msg.content}</div>
        <div class="message-time" style="font-size: 10px; color: #777; margin-top: 4px;">
            ${time}
        </div>
    `;

    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function loadHistory() {
    try {
        const res = await fetch(`${HTTP_URL}/chat/history?limit=50`);
        if (!res.ok) throw new Error(`HTTP status mismatch: ${res.status}`);
        const data = await res.json();

        messagesDiv.innerHTML = "";
        data.forEach(appendMessage);
    } catch (err) {
        console.error("Could not fetch historical telemetry records from database:", err);
    }
}
loadHistory();

function sendMessage() {
    const username = usernameInput.value.trim();
    const content = messageInput.value.trim();

    if (!username || !content) return;

    if (socket.readyState !== WebSocket.OPEN) {
        console.error("Transmission blocked: Client state socket connection remains inactive.");
        return;
    }

    const msg = {
        username,
        content,
        timestamp: new Date().toISOString()
    };

    socket.send(JSON.stringify(msg));
    messageInput.value = "";
}

sendButton.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});
