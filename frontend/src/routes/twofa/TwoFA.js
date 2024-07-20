import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, toggleHidden } from "../../utils/utils.js";
import { twofaUrl } from "../../contants/contants.js";

export async function fetch2FA() {

const form = document.getElementById("2fa-code");

form.addEventListener("submit", (e) => {

    e.preventDefault();
    const code = document.getElementById("code").value;
    const fields_warning = document.getElementById('fields-warning');

    if (!code)
    {
        insertIntoElement('fields-warning', "code shouldn't be empty");
        return;
    }
    toggleHidden('2fa-code');
    toggleHidden('login-spinner');

    fetch(twofaUrl, {
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
        document.getElementById('nav-bar').style.display = 'flex';
        return res.json();
    })
    .then(data => {
        localStorage.setItem("access_token", data.data.access_token);
        localStorage.setItem("refresh_token", data.data.refresh_token);
        navigateTo("/");
    })
    .catch((err) => {
        toggleHidden('2fa-code');
        toggleHidden('login-spinner');
    });

    localStorage.removeItem("email");
})
}
