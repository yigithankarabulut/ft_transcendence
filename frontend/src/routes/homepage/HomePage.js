import { navigateTo } from "../../utils/navTo.js";

document.addEventListener("DOMContentLoaded", function() {
    console.log("test1");
    const quickPlayButton = document.getElementById("quickplay-btn");
    const gameButtonContainer = document.getElementById("game-button-container");

    if (quickPlayButton) {
        quickPlayButton.addEventListener("click", function(event) {
            event.preventDefault();  // Prevent the default button behavior
            // Replace the GAME button with the game mode buttons
            gameButtonContainer.innerHTML = `
                <button id="two-player-btn" class="btn btn-primary">2 Players</button>
                <button id="four-player-btn" class="btn btn-primary">4 Players</button>
                <button id="eight-player-btn" class="btn btn-primary">8 Players</button>
            `;

            document.getElementById("two-player-btn").addEventListener("click", function() {
                navigateTo("/game?mode=2");
            });

            document.getElementById("four-player-btn").addEventListener("click", function() {
                navigateTo("/game?mode=4");
            });

            document.getElementById("eight-player-btn").addEventListener("click", function() {
                navigateTo("/game?mode=8");
            });
        });
    }
});
