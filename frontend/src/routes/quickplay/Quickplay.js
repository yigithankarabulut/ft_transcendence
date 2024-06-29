import { navigateTo } from "../../utils/navTo.js";

console.log("Quickplay.js loaded");

let gameData = {};

function initFormHandler() {
    console.log("DOM loaded");

    const form = document.querySelector(".requires-validation");
    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            event.stopPropagation();

            if (form.checkValidity()) {
                const roomLimit = document.querySelector('input[name="room_limit"]').value;
                const gameScore = document.querySelector('input[name="game_score"]').value;
                const players = document.querySelector('input[name="players"]').value.split(',').map(player => player.trim());

                gameData = {
                    room_limit: parseInt(roomLimit, 10),
                    game_score: parseInt(gameScore, 10),
                    players: players
                };

                console.log(JSON.stringify(gameData));

                fetch("http://127.0.0.1:8000/game/create", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(gameData),
                })
                .then(res => res.json())
                .then(responseData => {
                    if (responseData.room_name) {
                        gameData.room_name = responseData.room_name;
                        navigateTo("/game");
                    } else {
                        console.error("Failed to create room");
                    }
                })
                .catch(err => {
                    console.error("Error creating room:", err);
                });
            }

            form.classList.add('was-validated');
        }, false);
    } else {
        console.log("Form not found, retrying...");
        setTimeout(initFormHandler, 100);
    }
}

initFormHandler();

export { gameData };  //verileri diğer dosyalara aktarmak için
