import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement } from "../../utils/utils.js";
import { gameCreateUrl } from "../../contants/contants.js";

export async function fetchQuickplay() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        navigateTo("/login");
        return;
    }
    else {
    console.log("fetchingquickplay");
    const form = document.querySelector(".requires-validation2");
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        event.stopPropagation();
        const fields_warning = document.getElementById('fields-warning');

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
            fetch(gameCreateUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + access_token,
                },
                body: JSON.stringify(data),
            }).then(res => {
                if (!res.ok) {
                    return res.json().then(errorData => {
                        throw errorData;
                    });
                }
                return res.json();
            }).then(data => {
                localStorage.setItem("game_id", data.data.game_id);
                navigateTo("/game");
            }).catch((err) => {
                if (err.error) {
                    console.error(err.error);
                    insertIntoElement('fields-warning', "Error: " + err.error);
                }else if (err.non_field_errors)
                insertIntoElement('fields-warning', "Error: " + err.error);
            });
        }
        form.classList.add('was-validated');
    }, false);

    const form2 = document.querySelector(".requires-validation");
    form2.addEventListener("submit", function (event) {
        event.preventDefault();
        event.stopPropagation();
        const fields_warning_one = document.getElementById('fields-warning-one');

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
                    "Authorization": "Bearer " + access_token,
                },
                body: JSON.stringify(data),
            }).then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw errorData;
                    });
                }
                return response.json();
            }).then(data => {
                localStorage.setItem("game_id", data.data.game_id);
                navigateTo("/game");
            }).catch((err) => {
            console.error(err.error);
            insertIntoElement('fields-warning-one', "Error: " + err.error);
            });
        }
        form2.classList.add('was-validated');
    }, false);
}
}
