import { navigateTo } from "./src/utils/navTo.js";

// Display the navigation bar
document.getElementById('nav-bar').style.display = 'flex';

document.addEventListener("DOMContentLoaded", () => {
    const playButton = document.querySelector(".button-container a");
    if (playButton) {
        playButton.addEventListener("click", (e) => {
            e.preventDefault();
            // Start the game logic here
            console.log("Game is starting...");
            navigateTo("/quickplay");
        });
    }
});
