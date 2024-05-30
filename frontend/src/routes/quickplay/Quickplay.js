let button = document.getElementById('connect');
let userUrl = 'http://localhost:8000/user/details';
let acceptButton = document.getElementById('accept-button');
let token = localStorage.getItem('access_token');

if (!token) {
    navigateTo('/login');
}

fetch(userUrl, {
    method: 'GET',
    headers: {"Authorization": `Bearer ${token}`}
}).then(res => {
    if (!res.ok) {
        throw new Error('Error');
    }
    return res.json();
}).then(data => {
    console.log(data[0].message);
    if (data[0].message === "User found") {
        let ws = new WebSocket('ws://localhost:8008/ws/quickplay/' + token + '/');
        ws.onopen = () => {
            console.log('connected');
        }
        ws.onmessage = (e) => {
            console.log(e.data);
            let data = JSON.parse(e.data);
            if (data == "match found") {
                console.log("Match found");
                acceptButton.style.display = 'block';
                acceptButton.onclick = () => {
                    ws.send("accept");
                    acceptButton.style.display = 'none';
                }
            } else if (data == "start game") {
                // Burada oyun WebSocket bağlantısını başlatabilirsiniz
                startGameWebSocket(token);
            }
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
}).catch(err => {
    console.log(err);
    return ;
})

function startGameWebSocket(token) {
    console.log("Starting game...");
}
