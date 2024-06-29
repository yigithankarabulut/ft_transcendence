import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden, insertIntoElement } from "../../utils/utils.js";

const friendsUrl = "http://127.0.0.1:8000/friends"; // Replace with actual API endpoint

document.getElementById('nav-bar').style.display = 'flex';

export async function fetchFriends() {
    toggleHidden('home-spinner');
    try {
        const response = await fetch(friendsUrl, {
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
        const friends = data.friends; // Assuming the API returns an array of friends

        const friendsContainer = document.getElementById('friends');
        friendsContainer.innerHTML = ''; // Clear previous content

        friends.forEach(friend => {
            const friendElement = document.createElement('div');
            friendElement.classList.add('friend-card');
            friendElement.innerHTML = `
                <h2>${friend.name}</h2>
                <p>${friend.bio}</p>
                <img src="${friend.avatar}" alt="${friend.name}'s avatar" width="100">
            `;
            friendsContainer.appendChild(friendElement);
        });

        toggleHidden('home-spinner');
    } catch (err) {
        console.log(err);
        if (err.error === "Unauthorized" || err.error === "Token has expired") {
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
