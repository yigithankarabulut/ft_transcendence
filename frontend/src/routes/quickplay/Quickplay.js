import { navigateTo } from "../../utils/navTo.js";

export async function fetchQuickplay() {
    console.log("fetchingquickplay");
    const form = document.querySelector(".requires-validation");
    const form2 = document.querySelector(".requires-validation2");

    form2.addEventListener("submit", function (event) {
        event.preventDefault();
        event.stopPropagation();

        if (form2.checkValidity()) {
            const roomId = document.querySelector('input[name="roomId"]').value;
            const data = {
                roomId: roomId
            };
            localStorage.setItem("roomId", roomId);
            navigateTo("/game");
        }
        form2.classList.add('was-validated');
    }
    );
    
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        event.stopPropagation();

        if (form.checkValidity()) {
            const roomLimit = document.querySelector('input[name="room_limit"]').value;
            const gameScore = document.querySelector('input[name="game_score"]').value;
            const roomId = document.querySelector('input[name="roomId"]').value;

            const data = {
                room_limit: parseInt(roomLimit, 10),
                game_score: parseInt(gameScore, 10),
                roomId: roomId
            };

            // JSON verisini console'da görüntüleyin
            console.log(JSON.stringify(data));

            // Veriyi localStorage'e kaydedin
            localStorage.setItem("gameData", JSON.stringify(data));
            // room idyi local storage ekle ve backende bildir
            localStorage.setItem("roomId", roomId);

            // `game.js` dosyasına yönlendirin
            navigateTo("/game");
        }

        form.classList.add('was-validated');
    }, false);
}

