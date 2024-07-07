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

export async function onlineStatus() {
    let userId = 0;

    async function getUserId() {
        const userDetailUrl = "http://127.0.0.1:8000/user/details";
        const access_token = localStorage.getItem("access_token");

        await fetch(userDetailUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,
            }
        }).then(response => {
            if (!response.ok) {
                const errorData = response.json();
                throw new Error(errorData.error);
            }
            return response.json();
        }).then(data => {
            const user = data[0].data[0];
            userId = user.id;
        }).catch(err => {
            console.error(err);
        });
    }

    async function initializeWebSocket() {
        await getUserId();
        socket = new WebSocket(`ws://localhost:8020/ws/status/?user_id=${userId}`);
        socket.onopen = function (event) {
            console.log('WebSocket status connection opened');
        };
        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            console.log('WebSocket status message received:', data);
        };
        socket.onclose = function (event) {
            console.log('WebSocket status connection closed');
        };
        socket.onerror = function (error) {
            console.error('WebSocket status error:', error);
        };
        window.addEventListener('beforeunload', function () {
            socket.close();
        });
        window.addEventListener('online', function () {
            if (socket.readyState === WebSocket.CLOSED) {
                socket = new WebSocket(`ws://localhost:8020/ws/status/?user_id=${userId}`);
            }
        });
        window.addEventListener('offline', function () {
            socket.close();
        });
    }

    if (!localStorage.getItem("access_token")) {
        throw new Error("unauthorized");
    }
    if (socket && socket.readyState === WebSocket.OPEN) {
        return;
    }
    await initializeWebSocket()
}
