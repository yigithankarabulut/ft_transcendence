import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden, insertIntoElement } from "../../utils/utils.js";

const friendsUrl = "http://127.0.0.1:8000/user/search"; // Replace with actual API endpoint

document.getElementById('nav-bar').style.display = 'flex';

fetchFriends();

export async function fetchFriends() {
    console.log("Fetching friends")
    const token = localStorage.getItem("access_token");
    if (!token) {
        navigateTo("/login");
        return;
    }
    toggleHidden('home-spinner');
    try {
        const response = await fetch(friendsUrl + "?key=y", {
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
        console.log("Data: ", data);
        const friends = data[0].data;

        const friendsContainer = document.getElementById('friends');
        friendsContainer.innerHTML = ''; // Clear previous content

        friends.forEach(friend => {
            const friendElement = document.createElement('div');
            friendElement.classList.add('friend-card');
            friendElement.innerHTML = `
                <h2>${friend.first_name}</h2>
                <p>${friend.username}</p>
                <img src="${friend.avatar}" alt="${friend.name}'s avatar" width="100">
            `;
            friendsContainer.appendChild(friendElement);
        });

        toggleHidden('home-spinner');
    } catch (err) {
        console.log(err);
        if (err.error === "Unauthorized" || err.error === "Token has expired" || err.error === "Invalid token") {
            navigateTo("/login");
        } else if (err.error) {
            console.error("Error: ", err.error);
        } else {
            console.error("Error: internal server error");
        }
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    await fetchFriends();
});
