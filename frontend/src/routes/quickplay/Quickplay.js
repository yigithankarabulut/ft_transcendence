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
            if (e.data === 'match found') {
                acceptButton.style.display = 'block';
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

