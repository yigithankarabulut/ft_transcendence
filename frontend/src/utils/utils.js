import{ ValidateAccessToken, ValidateRefreshToken, userDetailUrl, StatusServiceSocketUrl } from "../constants/constants.js";

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
export let userStatuses = [];
let userId;

export async function onlineStatus() {
    if (!localStorage.getItem('access_token')) {
        return;
    }
    try {
        const response = await fetch(userDetailUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            }
        });
        if (!response.ok) {
            const errorData = await response.json();
            if (response.status === 401) {
                if (errorData.error === 'Token has expired') {
                    await RefreshToken();
                    return onlineStatus();
                }
                document.getElementById("logout-button").click();
                return;
            } else {
                throw new Error(errorData.error);
            }
        }
        const data = await response.json();
        const user = data.data[0];
        userId = user.id;

        // Eğer mevcut bir WebSocket bağlantısı varsa yeni bir bağlantı kurmayın
        if (socket && socket.readyState === WebSocket.OPEN) {
            // Server'dan online_users listesini iste
            socket.send(JSON.stringify({ type: 'getOnlineUsers' }));
            return;
        }
        socket = new WebSocket(StatusServiceSocketUrl + "?user_id=" + userId);
        socket.onopen = function (event) {
            localStorage.setItem('status', 'Online');

        };
        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            userStatuses = data.online_users;
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

    } catch (error) {
        console.error('Error: ', error);
        if (error.message === 'Token has expired') {
            await RefreshToken();
            return onlineStatus(); // Retry after token refresh
        }
    }
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
            try {
                await onClick(currentPage);
            } catch (error) {
                if (error.message === "Token has expired") {
                    await RefreshToken();
                    await onClick(currentPage);
                }
            }
        }
    });
    paginationContainer.appendChild(prevButton);
    // Create page number buttons
    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement("li");
        pageButton.innerHTML = `<li class="page-item ${i === currentPage ? "active" : ""}"><a href="#" class="page-link">${i}</a></li>`;
        pageButton.addEventListener("click", async (event) => {
            event.preventDefault();
            try {
                await onClick(i);
            } catch (error) {
                if (error.message === "Token has expired") {
                    await RefreshToken();
                    await onClick(i);
                }
            }
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
            try {
                await onClick(currentPage);
            } catch (error) {
                if (error.message === "Token has expired") {
                    await RefreshToken();
                    await onClick(currentPage);
                }
            }
        }
    });
    paginationContainer.appendChild(nextButton);
}

export async function CheckAuth() {
    const access_token = localStorage.getItem("access_token")
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
    if (data && data.user_id) {
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

    if (data && data.user_id) {
        return data.user_id;
    } else {
        return false;
    }
}
