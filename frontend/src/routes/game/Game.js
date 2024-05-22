import { navigateTo } from "../../utils/navTo.js";
let button = document.getElementById('connect');

let userUrl = 'http://localhost:8000/user/details';

button.addEventListener('click', () => {
    let token = localStorage.getItem('token');
    if (!token) {
        navigateTo('/game');
    }
    fetch(userUrl, {
        method: 'GET',
        headers: {"Authorization": `Bearer ${token}`}
    })
    .then(res => {
        if (!res.ok) {
            throw new Error('Error');
        }
        return res.json();
    })
    .then(data => {
        console.log(data[0].message);
        if (data[0].message === "User found") {
            var username = data[0].data[0].username;
            let ws = new WebSocket('ws://localhost:8008/ws/quickplay/' + username + '/');
        
            ws.onopen = () => {
                console.log('connected');
            }
        
            ws.onmessage = (e) => {
                console.log(e.data);
                // navigateTo('/game');
            }
        
            ws.onclose = () => {
                console.log('disconnected');
            }
            ws.onerror = (e) => {
                console.log(e);
            }
        } else {
            console.log("User not found");
            return;
        }
    })
    .catch(err => {
        console.log(err);
        return ;
    })

})


