import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, appendToElement, toggleHidden } from "../../utils/utils.js";

const homeContainer = document.getElementById("home-container");
const userDetailUrl = "http://127.0.0.1:8000/user/details";

export async function fetchUserDetails() {
    const token = localStorage.getItem("token");
    if (!token) {
        navigateTo("/login");
    }
    console.log("token: ", token);
    toggleHidden('home-spinner');
    fetch(userDetailUrl, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        }
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
        console.log(data)
        document.getElementById('user-fullname').innerText = data[0].data[0].first_name + " " + data[0].data[0].last_name;
        document.getElementById('user-name').innerText = data[0].data[0].username;
        document.getElementById('user-email').innerText = data[0].data[0].email;
    })
    .catch(err => {
        if (err.error) {
            console.log(err.error);
        }
        else {
            console.log("Error: internal server error", err);
        }
    });

};