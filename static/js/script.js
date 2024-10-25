const sendMessageButton = document.getElementById('sendMessageButton');
const messageInput = document.getElementById('messageInput');
const chatMessages = document.getElementById('chatMessages');

// Function to add a message to the chat display
function addMessage(user, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message');
    messageElement.innerHTML = `<span class="message-user">${user}</span>: <span class="message-text">${message}</span>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the latest message
}

// Event listener for when the send button is clicked
sendMessageButton.addEventListener('click', () => {
	const message = messageInput.value.trim(); // Get the message input value 
	if (message) { 
        addMessage('You', message);
        messageInput.value = '';

        // Send the message to the server using a POST request
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message }) // Send the message in the request body
        })
        .catch(error => console.error('Error sending message:', error)); 
    }
});

messageInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter')
        sendMessageButton.click();
});

// Function to poll for new messages from the server
function pollMessages() {
    // Send a GET request to check for received messages
    fetch('/receive_message')
        .then(response => response.json())
        .then(data => {
            if (data.message) { // If there's a message in the response
                addMessage('Peer', data.message); // Add the peer's message to the chat
            }
        })
        .catch(error => console.error('Error receiving message:', error)); 
}

setInterval(pollMessages, 200);
