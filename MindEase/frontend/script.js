// Handle sending message to backend
async function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  const chatBox = document.getElementById("chatBox");
  const typing = document.getElementById("typing");

  if (!message) return;

  appendMessage("You", message, "user");  // Show user message
  input.value = "";
  typing.style.display = "block";         // Show typing indicator

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    if (!response.ok) throw new Error("Server error");

    const data = await response.json();
    const botReply = `${data.reply} (Mood: ${data.mood})`;
    appendMessage("MindEase", botReply, "bot");  // Show bot message
  } catch (error) {
    console.error("Error:", error);
    appendMessage("MindEase", "🚫 Sorry, I’m having trouble responding right now.", "bot");
  } finally {
    typing.style.display = "none";
    chatBox.scrollTop = chatBox.scrollHeight;
  }
}

// Append message bubble to chat
function appendMessage(sender, text, cls) {
  const chat = document.getElementById("chatBox");
  const msg = document.createElement("div");
  msg.className = `msg ${cls}`;
  msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}

// Allow sending with keyboard Enter
document.getElementById("userInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});