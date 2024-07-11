export const insertIntoElement = (elementId, element) => {
    const el = document.getElementById(elementId);
    if (el)
        el.innerHTML = element;
}

export const appendToElement = (elementId, element) => {
    const el = document.getElementById(elementId);
    if (el)
        el.append(element);
}

export const toggleHidden = (elementId) => {
    const el = document.getElementById(elementId);
    if (el)
    {
        if (el.classList.contains("d-none")) {
            el.classList.remove('d-none');
            el.classList.add('block');
        }
        else {
            el.classList.add('d-none');
            el.classList.remove('block');
        }
    }
}



let socket = null;
export let userStatuses = {};

export async function onlineStatus() {
    let userId = 0;

    async function getUserId() {
        const userDetailUrl = "http://127.0.0.1:8000/user/details";
        const access_token = localStorage.getItem("access_token");
        const response = await fetch(userDetailUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,
            }
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error);
        }
        const data = await response.json();
        const user = data[0].data[0];
        userId = user.id;
    }

    async function initializeWebSocket() {
        if (localStorage.getItem("access_token")) {
            await getUserId();

            // Eğer mevcut bir WebSocket bağlantısı varsa yeni bir bağlantı kurmayın
            if (socket && socket.readyState === WebSocket.OPEN) {
                console.log('WebSocket connection already exists');

                // Server'dan online_users listesini iste
                socket.send(JSON.stringify({ type: 'getOnlineUsers' }));
                return;
            }
            socket = new WebSocket(`ws://localhost:8020/ws/status/?user_id=${userId}`);
            socket.onopen = function (event) {
                console.log('Connected to WebSocket');
                localStorage.setItem('status', 'Online');

            };
            socket.onmessage = function (event) {
                const data = JSON.parse(event.data);
                console.log('Message from server: ', data);
                userStatuses = data.online_users;
                console.log('Online users: ', userStatuses);
            };
            socket.onclose = function (event) {
                console.log('WebSocket connection closed');
            };
            socket.onerror = function (error) {
                console.error('WebSocket error: ', error);
            };
            window.addEventListener('beforeunload', function () {
                localStorage.setItem('status', 'Offline');
                socket.close();
            });
            window.addEventListener('online', function () {
                if (socket.readyState === WebSocket.CLOSED) {
                    socket = new WebSocket(`ws://localhost:8020/ws/status/?user_id=${userId}`);
                }
            });
            window.addEventListener('offline', function () {
                localStorage.setItem('status', 'Offline');
                socket.close();
            });
        }
    }

    await initializeWebSocket();
}

