import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden } from "../../utils/utils.js";


export async function fetchHomePage() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        console.log("No access token found");
        navigateTo("/login");
    } else {
        console.log("Access token found");
    }
}

export async function fetchAuth() {
    const urlParams = new URLSearchParams(window.location.search);
    const access_token = urlParams.get("access_token");
    const refresh_token = urlParams.get("refresh_token");

    if (access_token && refresh_token) {
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("refresh_token", refresh_token);
        navigateTo("/");
    } else {
        console.log("No access token found");
        navigateTo("/login");
    }
}