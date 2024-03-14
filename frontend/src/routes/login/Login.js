import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, appendToElement, toggleHidden } from "../../utils/utils.js";

const url = "http://localhost:8000/user/login";
const form = document.getElementById("login");

form.addEventListener("submit", (e) => {

    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const fields_warning = document.getElementById('fields-warning');

    if (!email  || !password)
    {
        insertIntoElement('fields-warning', "fields shouldn't be empty");
        return;
    }

    toggleHidden('login');
    // toggleHidden('login-spinner');

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: email,
            password: password,
        }),
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => {
                throw err;
            });
        }
        return res.json();
    })
    .then(data => {
        localStorage.setItem("email", email);
        navigateTo("/2fa");
    })
    .catch((err) => {
        console.log(err);
        if (err.error) {
            fields_warning.innerText = "Error: " + err.error;}
        else if (err.email) {
            fields_warning.innerText = "Email error: " + err.email[0];
        } else if (err.password) {
            fields_warning.innerText = "Password error: " + err.password[0];
        } else {
            fields_warning.innerText = "Error: internal server error";
        }
        toggleHidden('login');
        // toggleHidden('login-spinner');
    })
})
