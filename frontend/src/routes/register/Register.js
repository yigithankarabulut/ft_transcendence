import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, toggleHidden } from "../../utils/utils.js";

const url = "http://127.0.0.1:8000/user/register";
const form = document.getElementById("register");

form.addEventListener("submit", (e) => {

    e.preventDefault();
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const firstname = document.getElementById("firstname").value;
    const lastname = document.getElementById("lastname").value;
    const phone = document.getElementById("phone").value;
    const fields_warning = document.getElementById('fields-warning');

    if (!username || !email  || !password || !firstname || !lastname)
    {
        insertIntoElement('fields-warning', "fields shouldn't be empty");
        return;
    }

    toggleHidden('register');
    toggleHidden('register-spinner');

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
            first_name: firstname,
            last_name: lastname,
            phone: phone,
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
        localStorage.setItem("username", username);
        navigateTo("/login");
    })
    .catch((err) => {
    if (err.error) {
        fields_warning.innerText = "Error: " + err.error;
    }
    else if (err.password) {
        fields_warning.innerText = "Password error: " + err.password[0];
    } else if (err.phone) {
        fields_warning.innerText = "Phone error: " + err.phone[0];
    } else if (err.email) {
        fields_warning.innerText = "Email error: " + err.email[0];
    } else if (err.username) {
        fields_warning.innerText =  "Username error: " + err.username[0];
    } else {
        fields_warning.innerText = "Error: internal server error";
    }
    toggleHidden('register');
    toggleHidden('register-spinner');
    })
})