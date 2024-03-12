import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, appendToElement, toggleHidden } from "../../utils/utils.js";

const homeContainer = document.getElementById("home-container");
const userDetailUrl = "http://127.0.0.1:8000/user/detail";

function fetchUserDetails() {
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
            "Authorization": `Token ${token}`
        }
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("couldn't fetch user details");
        }
        return res.json();
    })
    .then(data => {
        console.log(data)
        toggleHidden('home-spinner');
        document.getElementById('user-fullname').innerText = data.first_name + " " + data.last_name;
        document.getElementById('user-name').innerText = data.username;
        document.getElementById('user-email').innerText = data.email;
    })
    .catch(err => {
        console.log(err);
    });

};