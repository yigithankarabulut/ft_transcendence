import { navigateTo } from "../../utils/navTo.js";
const gameCreateUrl = "http://127.0.0.1:8000/game/room";
export async function fetchQuickplay() {

    console.log("fetchingquickplay");
    const form = document.querySelector(".requires-validation2");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        event.stopPropagation();
        if (form.checkValidity()) {
            const user2 = document.querySelector('input[name="user2"]').value;
            const user3 = document.querySelector('input[name="user3"]').value;
            const user4 = document.querySelector('input[name="user4"]').value;

            const data = {
                room_limit: 4,
                players: [
                    user2,
                    user3,
                    user4
                ]
            };
            // JSON verisini console'da görüntüleyin
            fetch(gameCreateUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "authorization": "Bearer " + localStorage.getItem("access_token"),
                },
                body: JSON.stringify(data),
            }).then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to create game room");
                }
                return response.json();
            }
            ).then((data) => {
                console.log(data);
            }).catch((error) => {
                console.error(error);
            })
        }
        form.classList.add('was-validated');
    }, false);

    const form2 = document.querySelector(".requires-validation");

    form2.addEventListener("submit", function (event) {
        event.preventDefault();
        event.stopPropagation();

        if (form2.checkValidity()) {
            const user5 = document.querySelector('input[name="user5"]').value;
            const data = {
                room_limit: 2,
                players: [
                    user5
                ]
            };
            fetch(gameCreateUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem("access_token"),
                },
                body: JSON.stringify(data),
            }).then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to create game room");
                }
                return response.json();
            }
            ).then((data) => {
                localStorage.setItem("game_id", data.data.game_id);
                navigateTo("/game");
            }).catch((error) => {
                console.error(error);
            })
        }
        form2.classList.add('was-validated');
    }, false);
}

