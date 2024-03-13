import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden,  insertIntoElement } from "../../utils/utils.js";

const userDetailUrl = "http://127.0.0.1:8000/user/details";

export async function fetchUserDetails() {
    const token = localStorage.getItem("token");
    if (!token) {
        navigateTo("/login");
        return;
    }
    toggleHidden('home-spinner');
    try {
        const response = await fetch(userDetailUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error);
        }

        const data = await response.json();
        const user = data[0].data[0];
        const fullname = document.getElementById('fullname')
        const username = document.getElementById('username');
        const email = document.getElementById('email');

        insertIntoElement('fullname', user.fullname);
        insertIntoElement('username', user.username);
        insertIntoElement('email', user.email);
        toggleHidden('fullname');
        toggleHidden('home-spinner');
    } catch (err) {
        console.log(err);
        if (err.error === "Unauthorized") {
            navigateTo("/login");
        } else if (err.error === "Token has expired") {
            navigateTo("/login");
        } else if (err.error) {
            console.error("Error: ", err.error);
        } else {
            console.error("Error: internal server error");
        }
    }
}
