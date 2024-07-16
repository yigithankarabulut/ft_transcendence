import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, toggleHidden } from "../../utils/utils.js";

const url = "http://127.0.0.1:8000/user/username";

export async function fetchConflictusername() {
    const form = document.getElementById("uname-code");
    
    const urlParams = new URLSearchParams(window.location.search);
    const access_token = urlParams.get("access_token");
    const refresh_token = urlParams.get("refresh_token");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const fields_warning = document.getElementById('fields-warning');
        if (!username) {
            insertIntoElement('fields-warning', "Username shouldn't be empty");
            return;
        }
        toggleHidden('uname-code');
        toggleHidden('login-spinner');

        try {
            const response = await fetch(url, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`,
                },
                body: JSON.stringify({
                    username: username,
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw errorData;
            }
            localStorage.setItem("access_token", access_token);
            localStorage.setItem("refresh_token", refresh_token);
            navigateTo("/");
        } catch (err) {
            console.log("123123123123123", err);
            if (err.error) {
                insertIntoElement('fields-warning', "Error: " + err.error);
            } else if (err.username) {
                insertIntoElement('fields-warning', "Username error: " + err.username);
            }
            toggleHidden('uname-code');
            toggleHidden('login-spinner');
        }
    });
}
