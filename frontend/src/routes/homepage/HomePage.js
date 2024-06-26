import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden, insertIntoElement } from "../../utils/utils.js";

const userDetailUrl = "http://127.0.0.1:8000/user/details";
document.getElementById('nav-bar').style.display = 'flex';

document.addEventListener("DOMContentLoaded", () => {
    const optionsButton = document.getElementById("options-button");
    const twoPlayerButton = document.getElementById("two-player-button");
    const fourPlayerButton = document.getElementById("four-player-button");
    const quickplayButton = document.getElementById("quickplay-button");
    const inviteButton = document.getElementById("invite-button");

    optionsButton.addEventListener("click", () => {
        optionsButton.classList.add("hidden");
        twoPlayerButton.classList.remove("hidden");
        fourPlayerButton.classList.remove("hidden");
    });

    twoPlayerButton.addEventListener("click", (e) => {
        e.preventDefault();
        twoPlayerButton.classList.add("hidden");
        fourPlayerButton.classList.add("hidden");
        quickplayButton.classList.remove("hidden");
        inviteButton.classList.remove("hidden");
    });

    quickplayButton.addEventListener("click", (e) => {
        e.preventDefault();
        navigateTo("/quickplay");
    });

    inviteButton.addEventListener("click", (e) => {
        e.preventDefault();
        // Add your invite logic here
        console.log("Invite selected");
    });

    // You can add functionality for the 4 Player button as needed
    fourPlayerButton.addEventListener("click", (e) => {
        e.preventDefault();
        // Add your 4 player logic here
        console.log("4 Player selected");
    });
});

export async function fetchUserDetails() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        navigateTo("/login");
        return;
    }
    toggleHidden('home-spinner');
    try {
        const response = await fetch(userDetailUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error);
        }

        const data = await response.json();
        const user = data[0].data[0];
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
