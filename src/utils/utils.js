import{ ValidateAccessToken, ValidateRefreshToken, userDetailUrl, StatusServiceSocketUrl } from "../contants/contants.js";

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

export let socket = null;
export let userStatuses = {};

export async function onlineStatus() {
    let userId = await CheckAuth();
    console.log('User ID: ', userId);
    if (!userId) {
        return;
    }
    // Eğer mevcut bir WebSocket bağlantısı varsa yeni bir bağlantı kurmayın
    if (socket && socket.readyState === WebSocket.OPEN) {
        console.log('WebSocket connection already exists');

        // Server'dan online_users listesini iste
        socket.send(JSON.stringify({ type: 'getOnlineUsers' }));
        return;
    }
    socket = new WebSocket(StatusServiceSocketUrl + "?user_id=" + userId);
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
            socket = new WebSocket(StatusServiceSocketUrl + "?user_id=" + userId);
        }
    });
    window.addEventListener('offline', function () {
        localStorage.setItem('status', 'Offline');
        socket.close();
    });
}



export function goPagination(totalPages, currentPage, onClick, elementId) {
    const paginationContainer = document.getElementById(elementId);
    paginationContainer.innerHTML = "";
    // Create previous button
    const prevButton = document.createElement("li");
    prevButton.innerHTML = `<li class="page-item ${currentPage === 1 ? "disabled" : ""}"><a href="#" class="page-link">&laquo;</a></li>`;
    prevButton.addEventListener("click", async (event) => {
        event.preventDefault();
        if (currentPage > 1) {
            currentPage--;
            onClick(currentPage);
        }
    });
    paginationContainer.appendChild(prevButton);
    // Create page number buttons
    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement("li");
        pageButton.innerHTML = `<li class="page-item ${i === currentPage ? "active" : ""}"><a href="#" class="page-link">${i}</a></li>`;
        pageButton.addEventListener("click", async (event) => {
            event.preventDefault();
            onClick(i);
        });
        paginationContainer.appendChild(pageButton);
    }
    // Create next button
    const nextButton = document.createElement("li");
    nextButton.innerHTML = `<li class="page-item ${currentPage === totalPages ? "disabled" : ""}"><a href="#" class="page-link">&raquo;</a></li>`;
    nextButton.addEventListener("click", async (event) => {
        event.preventDefault();
        if (currentPage < totalPages) {
            currentPage++;
            onClick(currentPage);
        }
    });
    paginationContainer.appendChild(nextButton);
}

export async function CheckAuth() {

    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        return false;
    }
    const auth_response = await fetch(ValidateAccessToken, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${access_token}`,
        }
    });
    if (!auth_response.ok) {
        const errorData = await auth_response.json();
        if (auth_response.status === 401) {
            if (errorData.error === "Token has expired") {
                let state = await RefreshToken();
                if (state) {
                    return true;
                }
                return false;
            }
        }
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        return false;
    }
    const data = await auth_response.json();
    if (data.user_id) {
        return data.user_id;
    }
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    return false;
}

export async function RefreshToken() {
    const refresh_token = localStorage.getItem("refresh_token");
    const access_token = localStorage.getItem("access_token");
    if (!refresh_token) {
        return false;
    }
    const refresh_response = await fetch(ValidateRefreshToken, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${access_token}`,
        },
        body: JSON.stringify({ refresh_token: refresh_token })
    });

    if (!refresh_response.ok) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        return false;
    }

    const data = await refresh_response.json();
    if (!data.access_token || !data.refresh_token) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        return false;
    }
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    return refresh_response.data.user_id;
}
