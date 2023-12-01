document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("user-input");
  const chatMessages = document.getElementById("chat-messages");

  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const userMessage = chatInput.value;

    appendMessage("You", userMessage, "user");

    sendUserMessageToServer(userMessage);

    chatInput.value = "";
  });

  function appendMessage(sender, message, senderClass) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", senderClass);
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatMessages.appendChild(messageDiv);
  }

  function handleServerResponse(response) {
    appendMessage("Chatbot", response, "chatbot");
  }

  function sendUserMessageToServer(message) {
    const data = new FormData();
    data.append('response', message);
    data.append('question_id', 1);

    fetch('/submit/', {
      method: 'POST',
      body: data,
    })
      .then((response) => response.json())
      .then((data) => {
        handleServerResponse(data.response);
      })
      .catch((error) => {
        console.error('Error sending message:', error);
      });

    setTimeout(() => {
      const chatbotResponse = "Test message.";
      handleServerResponse(chatbotResponse);
    }, 1000); 
  }
});
