import { navigateTo } from "../../utils/navTo.js";
const userDetailUrl = "http://127.0.0.1:8000/user/details";
const gameDetailUrl = "http://127.0.0.1:8000/game/list";

export async function fetchJoin() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        navigateTo("/login");
        return;
    }
    console.log("Fetching user details");
    const response = await fetch(gameDetailUrl, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${access_token}`,
        }
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
    }

    const invites_res = await response.json();
    const invites = invites_res.data
    console.log(invites);
    const tbody = document.querySelector(".table tbody");
    tbody.innerHTML = ""; // Clear existing rows

    invites.forEach((invite, index) => {
        const row = document.createElement("tr");

        const th = document.createElement("th");
        th.scope = "row";
        th.innerText = index + 1;
        row.appendChild(th);

        const player = document.createElement("td");
        player.innerText = invite.player1; // Adjust based on actual user object
        row.appendChild(player);

        const room_id = document.createElement("td");
        room_id.innerText = invite.room_id; // Adjust based on actual user object
        row.appendChild(room_id);

        const buttonTd = document.createElement("td");
        const button = document.createElement("button");
        button.type = "button";
        button.className = "btn btn-primary";
        button.innerText = "Join";
        buttonTd.appendChild(button);
        row.appendChild(buttonTd);

        tbody.appendChild(row);

        button.addEventListener("click", async () => {
            console.log(invite);
            localStorage.setItem("game_id", invite.game_id);
            navigateTo("/game");
        });
    });
}
