document.addEventListener("DOMContentLoaded", () => {
    const messageInput = document.getElementById("message-input");
    const sendBtn = document.getElementById("send-btn");
    const chatWindow = document.getElementById("chat-window");

    const API_URL = "http://127.0.0.1:5000/predict"; // URL of your Flask backend

    function addMessage(sender, text) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message", `${sender}-message`);
        messageElement.textContent = text;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to the bottom
    }

    function showTypingIndicator() {
        const typingIndicator = document.createElement("div");
        typingIndicator.classList.add("chat-message", "bot-message");
        typingIndicator.innerHTML = `
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        typingIndicator.id = "typing-indicator";
        chatWindow.appendChild(typingIndicator);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function hideTypingIndicator() {
        const typingIndicator = document.getElementById("typing-indicator");
        if (typingIndicator) {
            chatWindow.removeChild(typingIndicator);
        }
    }

    async function handleUserMessage() {
        const messageText = messageInput.value.trim();
        if (messageText === "") return;

        addMessage("user", messageText);
        messageInput.value = "";
        showTypingIndicator();

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: messageText }),
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            hideTypingIndicator();
            addMessage("bot", data.answer);

        } catch (error) {
            hideTypingIndicator();
            addMessage("bot", "Sorry, something went wrong. Please try again later.");
            console.error("Error:", error);
        }
    }

    sendBtn.addEventListener("click", handleUserMessage);

    messageInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            handleUserMessage();
        }
    });

    // Initial bot message
    addMessage("bot", "Hello! I am your bank assistant. How can I help you today?");
});