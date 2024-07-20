import { navigateTo } from "../../utils/navTo.js";
import { wsInstance } from "../../sockets/BaseSocket.js";

var queryparams = new URLSearchParams(window.location.search);
if (queryparams.size != 2) {
    navigateTo('/');
}

var tournament = queryparams.get('name');
var username = queryparams.get('user');

if (!tournament || !username) {
    navigateTo('/');
}

console.log(tournament, username);
wsInstance.connect('ws://localhost:8009/ws/tournament/' + tournament + '/' + '?user=' + username);

// var ws;
// function openWebSocket() {
//     ws.onopen = () => {
//         console.log('connected');
//     }
//     ws.onmessage = (e) => {
//         console.log(e.data);
//     }
//     ws.onclose = () => {
//         console.log('disconnected');
//     }
//     ws.onerror = (e) => {
//         console.log(e);
//     }
// }
// // Only open the WebSocket connection if it's not already open
// if (!ws || ws.readyState !== WebSocket.OPEN) {
//     openWebSocket();
// }

document.getElementById('invite').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    console.log(username);
    var data = {
        "type": "adduser",
        "username": username
    }
    ws.send(JSON.stringify(data));
});

document.getElementById('start').addEventListener('click', function(event) {
    var data = {
        "type": "start"
    }
    ws.send(JSON.stringify(data));
});