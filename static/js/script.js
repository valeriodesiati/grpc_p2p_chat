const sendMessageButton = document.getElementById('sendMessageButton');
const messageInput = document.getElementById('messageInput');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');

// Function to add a message to the chat display
function addSendMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message');
    messageElement.innerHTML = `<span class="message-text-send">${message}</span>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the latest message
}

// Function to add a message to the chat display
function addReceivedMessage(user, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message');
    messageElement.innerHTML = `<span class="message-user-receive">${user}</span>: <span class="message-text-receive">${message}</span>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the latest message
}

// Event listener for when the send button is clicked
sendMessageButton.addEventListener('click', () => {
	const message = messageInput.value.trim(); // Get message from input
	const user = userInput.value.trim(); // Get username from input
	if (message && user) { 
        addSendMessage(message);
        messageInput.value = '';
        dataToSend = JSON.stringify({ user, message }); //JSONify username and message

        // Send a POST request with username and message in JSON format
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: dataToSend
        })
        .catch(error => console.error('Errore durante l\'invio del messaggio:', error)); 
    }
});

messageInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter')
        sendMessageButton.click();
});

function pollMessages() {
    fetch('/receive_message')
        .then(response => {
            if (response.status === 204) {
                console.log('No new messages');
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.user && data.message) {
                addReceivedMessage(data.user, data.message);
            }
        })
        .catch(error => console.error('Error receiving messages:', error));

}

setInterval(pollMessages, 200);
