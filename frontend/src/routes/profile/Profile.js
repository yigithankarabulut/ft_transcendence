import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden } from "../../utils/utils.js";

const userDetailUrl = "http://127.0.0.1:8000/user/details";
const updateUserUrl = "http://127.0.0.1:8000/user/update";

let originalUserData = {};

export async function fetchProfile() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        navigateTo("/login");
        return;
    }
    try {
        console.log("Fetching user details");
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
        console.log(user);
        const firstNameDiv = document.getElementById("full-name").textContent = `${user.first_name} ${user.last_name}`;

        setupwebSocket();//eklenen kısım

    } catch (err) {
        console.log(err);
    }
}

//buradan sonrası da eklenen kısımlardan
function setupWebSocket() {
    //start the WebSocket connection
    socket = new WebSocket(socketUrl);
    socket.onopen = function() {
        console.log("WebSocket connection opened");
        document.getElementById("profile-status").textContent = "Online";
    };

    socket.onclose = function() {
        console.log("WebSocket connection closed");
        document.getElementById("profile-status").textContent = "Offline";
    };

    socket.onerror = function(error) {
        console.error("WebSocket error:", error);
        document.getElementById("profile-status").textContent = "Offline";
    };
}

window.addEventListener("beforeunload", () => {
    if (socket) {
        socket.close();
    }
});
