import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, appendToElement, toggleHidden } from "../../utils/utils.js";


const url = "http://localhost:8004/user/login";
const form = document.getElementById("login");

form.addEventListener("submit", (e) => {

    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const loginContainer = document.getElementById("login-container");
    const fields_warning = document.getElementById('fields-warning');

    if (!email  || !password)
    {
        insertIntoElement('fields-warning', "fields shouldn't be empty");
        return;
    }

    toggleHidden('login');
    toggleHidden('login-spinner');

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: email,
            password: password,
        }),
    })
        .then(res => {
            if (!res.ok) {
                fields_warning.innerText = "invalid email or password";
                throw new Error("couldn't log in");
            }
            return res.json();
        })
        .then(token => {
            localStorage.setItem("jwt-token", token.access);
            localStorage.setItem("jwt-token-refresh", token.refresh);
            localStorage.setItem("email", email);
            navigateTo("/2fa");
        })
        .catch((err) => {
            toggleHidden('login');
            toggleHidden('login-spinner');

        })
})
