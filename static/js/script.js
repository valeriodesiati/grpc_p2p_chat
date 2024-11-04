const sendMessageButton = document.getElementById('sendMessageButton');
const messageInput = document.getElementById('messageInput');
const userInput = document.getElementById('userInput');
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
	const message = messageInput.value.trim(); // Get message from input
	const user = userInput.value.trim(); // Get username from input
	if (message && user) { 
        addMessage(user, message);
        messageInput.value = '';
        dataToSend = JSON.stringify({ user, message }); //JSONify username and message
        console.log("data to send" + dataToSend);

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

// Function to poll for new messages from the server
function pollMessages() {
    // Send a GET request to check for received messages
    fetch('/receive_message')
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nella risposta del server');
            }
            return response.text(); // Gest the response in text format
        })
        .then(text => {
            if (text)
                console.log(text);
                const data = JSON.parse(text);
                if (data.user && data.message) { 
                    addMessage(data.user, data.message); // Display chat
                }
        })
        .catch(error => console.error('Error receiving message:', error)); 
}

setInterval(pollMessages, 200);