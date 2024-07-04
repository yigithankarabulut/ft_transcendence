import { navigateTo } from "../../utils/navTo.js";

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
            console.log(JSON.stringify(data));
            // data backe gidecek backten donene gore navto calisir

            // navigateTo("/game");
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
            console.log(JSON.stringify(data));
            //yigite gonderilecek
            // navigateTo("/game");
        }
        form2.classList.add('was-validated');
    }, false);
}

