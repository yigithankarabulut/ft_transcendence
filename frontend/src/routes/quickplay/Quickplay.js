import { navigateTo } from "../../utils/navTo.js";
import { RefreshToken, insertIntoElement } from "../../utils/utils.js";
import { gameCreateUrl } from "../../constants/constants.js";

export async function fetchQuickplay() {

    if (!localStorage.getItem("access_token")) {
        navigateTo("/login");
        return;
    }
    else {
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
            const postGameCreate = () => {
                return fetch(gameCreateUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify(data),
                });
            };
            const handleResponse = response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        if (response.status === 401 && errorData.error === "Token has expired") {
                            return RefreshToken().then(() => {
                                return postGameCreate().then(handleResponse);
                            });
                        } else {
                            throw errorData;
                        }
                    });
                }
                return response.json();
            };
            postGameCreate()
            .then(handleResponse)
            .then(data => {
                localStorage.setItem("game_id", data.data.game_id);
                navigateTo("/game");
            })
            .catch(err => {
                console.error(err.error);
                insertIntoElement('fields-warning-one', "Error: " + err.error);
            })
            .finally(() => {
                form.classList.add('was-validated');
            });
        } else {
                form.classList.add('was-validated');
            }
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

            const postGameCreate = () => {
                return fetch(gameCreateUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify(data),
                });
            };

            const handleResponse = response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        if (response.status === 401 && errorData.error === "Token has expired") {
                            return RefreshToken().then(() => {
                                return postGameCreate().then(handleResponse);
                            });
                        } else {
                            throw errorData;
                        }
                    });
                }
                return response.json();
            };
            postGameCreate()
                .then(handleResponse)
                .then(data => {
                    localStorage.setItem("game_id", data.data.game_id);
                    navigateTo("/game");
                })
                .catch(err => {
                    console.error(err.error);
                    insertIntoElement('fields-warning-one', "Error: " + err.error);
                })
                .finally(() => {
                    form2.classList.add('was-validated');
                });
        } else {
            form2.classList.add('was-validated');
        }
    }, false);

}
}
