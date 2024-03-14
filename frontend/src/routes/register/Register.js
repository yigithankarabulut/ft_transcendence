import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, toggleHidden } from "../../utils/utils.js";

const url = "http://127.0.0.1:8000/user/register";
const form = document.getElementById("register");
document.getElementById('nav-bar').style.display = 'none';

form.addEventListener("submit", (e) => {

    e.preventDefault();
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const firstname = document.getElementById("firstname").value;
    const lastname = document.getElementById("lastname").value;
    const phone = document.getElementById("phone").value;
    const fields_warning = document.getElementById('fields-warning');
    const fields_success = document.getElementById('fields-success');

    
    if (!username || !email  || !password || !firstname || !lastname)
    {
        insertIntoElement('fields-warning', "fields shouldn't be empty");
        return;
    }

    toggleHidden('register');
    // toggleHidden('register-spinner');

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
        setTimeout(() => {
            navigateTo("/login");
        }, 2000);
    })
    .catch((err) => {
        if (err.error) {
            insertIntoElement('fields-warning', "Error: " + err.error);
        } else if (err.username) {
            insertIntoElement('fields-warning', "Username error: " + err.username[0]);
        } else if (err.email) {
            insertIntoElement('fields-warning', "Email error: " + err.email[0]);
        } else if (err.phone) {
            insertIntoElement('fields-warning', "Phone error: " + err.phone[0]);
        } else if (err.password) {
            insertIntoElement('fields-warning', "Password error: " + err.password[0]);
        } else if (err.first_name) {
            insertIntoElement('fields-warning', "First name error: " + err.first_name[0]); 
        } else if (err.last_name) {
            insertIntoElement('fields-warning', "Last name error: " + err.last_name[0]);
        } else {
            insertIntoElement('fields-warning', "Error: internal server error");
            console.log(err);
        }
        // toggleHidden('fields-warning');
        toggleHidden('register');
        // toggleHidden('register-spinner');
    })
})