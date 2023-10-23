const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);

chatSocket.onopen = function (e) {
    console.log("CONNECTION ESTABLISHED");
}

chatSocket.onclose = function (e) {
    console.log("CONNECTION LOST");
}

chatSocket.onerror = function (e) {
    console.log("ERROR OCCURRED");
}