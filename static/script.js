
function toggleChatbot() {
    var chatbotPopup = document.getElementById("chatbotPopup");
    if (chatbotPopup.style.display === "none" || chatbotPopup.style.display === "") {
        chatbotPopup.style.display = "block";
    } else {
        chatbotPopup.style.display = "none";
    }
}

document.getElementById('chatForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const userInput = document.getElementById('userInput').value;
    const chatDiv = document.getElementById('chat');

    // Display the user's message
    chatDiv.innerHTML += `<div class="message user">You: ${userInput}</div>`;

    try {
        // Send the request to the FastAPI backend
        const response = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                context: "",  // You may want to maintain the context here
                question: userInput
            }),
        });

        const data = await response.json();

        // Display the bot's response
        chatDiv.innerHTML += `<div class="message bot">Bot: ${data.answer}</div>`;
    } catch (error) {
        console.error('Error:', error);
    }

    // Clear the input field
    document.getElementById('userInput').value = '';
});
