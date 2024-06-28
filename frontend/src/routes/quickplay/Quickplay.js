import { navigateTo } from './navTo.js';

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

