import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, appendToElement, toggleHidden } from "../../utils/utils.js";


const url = "http://127.0.0.1:8000/user/2fa";
const form = document.getElementById("2fa-code");

form.addEventListener("submit", (e) => {

    e.preventDefault();
    const code = document.getElementById("code").value;
    const loginContainer = document.getElementById("login-container");
    const fields_warning = document.getElementById('fields-warning');

    if (!code)
    {
        insertIntoElement('fields-warning', "code shouldn't be empty");
        return;
    }
    var email = localStorage.getItem("email");
    toggleHidden('2fa-code');
    toggleHidden('login-spinner');

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: localStorage.getItem("email"),
            twofa_code: code,
        }),
    })
    .then(res => {
        if (!res.ok) {
            fields_warning.innerText = "invalid code";
            throw new Error("couldn't log in");
        }
        return res.json();
    })
    .then(token => {
        localStorage.setItem("jwt-token", token.access);
        localStorage.setItem("jwt-token-refresh", token.refresh);
        console.log("token", token.access);
        console.log("token", token.refresh);
        navigateTo("/");
    })
    .catch((err) => {
        toggleHidden('2fa-code');
        toggleHidden('login-spinner');
    })
})
