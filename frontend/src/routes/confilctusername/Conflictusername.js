import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, toggleHidden } from "../../utils/utils.js";


const url = "http://127.0.0.1:8000/user/update/username";

export async function fetchConflictusername() {

const form = document.getElementById("uname-code");

form.addEventListener("submit", (e) => {

    e.preventDefault();
    const username = document.getElementById("username").value;
    const fields_warning = document.getElementById('fields-warning');
    const access_token = urlParams.get("access_token");
    const refresh_token = urlParams.get("refresh_token");

    if (!code)
    {
        insertIntoElement('fields-warning', "code shouldn't be empty");
        return;
    }
    toggleHidden('uname-code');
    toggleHidden('login-spinner');
    fetch(url, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${access_token}`,
        },
        body: JSON.stringify({
            username: username,
        }),
    })
    .then(res => {
        if (!res.ok) {
            fields_warning.innerText = "invalid username";
            throw new Error("couldn't log in");
        }
        document.getElementById('nav-bar').style.display = 'flex';
        return res.json();
    })
    .then(data => {
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("refresh_token", refresh_token);
        navigateTo("/");
    })
    .catch((err) => {
        toggleHidden('uname-code');
        toggleHidden('login-spinner');
    });
})
}
