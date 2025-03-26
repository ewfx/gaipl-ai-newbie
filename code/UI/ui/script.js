const chatLog = document.getElementById('chat-log');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const plusButton = document.getElementById('plus-button');
const incidentList = document.getElementById('incident-list');


function appendMessage(message, className) {
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    messageDiv.classList.add('message', className);
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll
}

function handleUserInput() {
    const message = userInput.value.trim();
    if (message) {
        appendMessage(message, 'user-message');
        userInput.value = '';

        // Simulate bot response (replace with your actual logic)
        setTimeout(() => {
            const botResponse = getBotResponse(message);
            appendMessage(botResponse, 'bot-message');
        }, 500); // Simulate delay
    }
}

function getBotResponse(userMessage) {
    const serverUrl = 'http://localhost:8081/chat'; // Replace with your server's URL
    var incident =
    fetch(serverUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }, ),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const botResponse = data.response; // Adjust this based on your server's response structure
        appendMessage(botResponse, 'bot-message');
    })
    .catch(error => {
        console.error('Error fetching bot response:', error);
        appendMessage('Sorry, there was an error communicating with the server.', 'bot-message');
    });
}


sendButton.addEventListener('click', handleUserInput);
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        handleUserInput();
    }
});

plusButton.addEventListener('click', () => {
            fetch('http://localhost:8081/incidents')
                .then(response => response.json())
                .then(incidents => {
                    incidentList.innerHTML= '';
                    if (incidents.length > 0) {
                        incidents.forEach(incident => {
                            const item = document.createElement('div');
                            item.textContent = incident.ticket_id + " - " + incident.problem_statement;
                            item.className = 'incident-item';
                            item.addEventListener('click', () => {
                                userInput.value += `+${incident.ticket_id}`;
                                incidentList.style.display = 'none';
                            });
                            incidentList.appendChild(item);
                        });
                        incidentList.style.display = 'block';
                        incidentList.style.left = plusButton.offsetLeft + plusButton.offsetWidth + 'px';
                        incidentList.style.top = plusButton.offsetTop + 'px';
                    } else {
                        incidentList.innerHTML = "No Incidents found";
                        incidentList.style.display = 'block';
                        incidentList.style.left = plusButton.offsetLeft + plusButton.offsetWidth + 'px';
                        incidentList.style.top = plusButton.offsetTop + 'px';
                    }

                })
                .catch(error => {
                    console.error('Error:', error);
                    incidentList.innerHTML = "Error loading incidents";
                    incidentList.style.display = 'block';
                    incidentList.style.left = plusButton.offsetLeft + plusButton.offsetWidth + 'px';
                    incidentList.style.top = plusButton.offsetTop + 'px';
                });
        });
  document.addEventListener('click', (event) => {
            if (!event.target.closest('#plus-button') && !event.target.closest('#incident-list')) {
                incidentList.style.display = 'none';
            }
        });