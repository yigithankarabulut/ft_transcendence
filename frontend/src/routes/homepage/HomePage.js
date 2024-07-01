import { navigateTo } from "../../utils/navTo.js";

document.getElementById('nav-bar').style.display = 'flex';

const access_token = localStorage.getItem("access_token");
if (!access_token) {
    console.log("No access token found");
    navigateTo("/login");
} else {
    console.log("Access token found");
}

document.getElementById('quickplay-btn').addEventListener('click', function() {
    navigateTo("/quickplay");
});

