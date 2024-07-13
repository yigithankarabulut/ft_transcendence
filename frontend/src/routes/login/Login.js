import { insertIntoElement, toggleHidden } from "../../utils/utils.js";
import  { navigateTo } from "../../utils/navTo.js";

const loginUrl = "http://127.0.0.1:8000/user/login";
const IntraOAuthUrl = "http://127.0.0.1:8000/auth/intra"

export async function fetchLogin() {

document.getElementById('login-form').addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email || !password) {
        insertIntoElement('fields-warning', "Fields shouldn't be empty");
        return;
    }
    toggleHidden('login-form');
    try {
        const response = await fetch(loginUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Internal server error");
        }
        const data = await response.json();
        localStorage.setItem("email", email);
        navigateTo("/2fa");
    } catch (err) {
        insertIntoElement('fields-warning', `Error: ${err.message}`);
        toggleHidden('login-form');
    }
});

document.getElementById('FtButton').addEventListener("click", () => {
    const response =  fetch(IntraOAuthUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    });
    response.then(res => {
        if (!res.ok) {
            return res.json().then(err => {
                throw err;
            });
        }

        res.json().then(data => {
            if (data.url) {
                window.location.replace(data.url);
            }
        });
    })
});
}