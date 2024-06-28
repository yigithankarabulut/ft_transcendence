import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden } from "../../utils/utils.js";

document.getElementById('nav-bar').style.display = 'flex';

const access_token = localStorage.getItem("access_token");
if (!access_token) {
    console.log("No access token found");
    navigateTo("/login");
} else {
    console.log("Access token found");

    toggleHidden('home-spinner');

    const handleButtonClick = (event) => {
        event.preventDefault();
        console.log("Button clicked");
    };

    const quickPlayButton = document.getElementById("quickplay-btn");
    if (quickPlayButton) {
        quickPlayButton.addEventListener("click", handleButtonClick);
    }

    document.addEventListener("DOMContentLoaded", function () {
        const form = document.querySelector(".requires-validation");

        form.addEventListener("submit", function (event) {
            event.preventDefault();
            event.stopPropagation();

            if (form.checkValidity()) {
                const roomLimit = document.querySelector('input[name="room_limit"]').value;
                const gameScore = document.querySelector('input[name="game_score"]').value;
                const players = document.querySelector('input[name="players"]').value.split(',').map(player => player.trim());

                const data = {
                    room_limit: parseInt(roomLimit, 10),
                    game_score: parseInt(gameScore, 10),
                    players: players
                };
                
                // JSON verisini console'da görüntüleyin
                console.log(JSON.stringify(data));
                // Veriyi localStorage'e kaydedin
                localStorage.setItem("gameData", JSON.stringify(data));
                // `game.js` dosyasına yönlendirin
                navigateTo("/game");
            }

            form.classList.add('was-validated');
        }, false);
    });
}
