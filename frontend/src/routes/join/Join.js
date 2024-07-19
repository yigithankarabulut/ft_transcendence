import { navigateTo } from "../../utils/navTo.js";
import { gameDetailUrl, joinUrl } from "../../constants/urls.js";
import { goPagination } from "../../utils/utils.js";

let currentPage = 1;

export async function fetchJoin() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        navigateTo("/login");
        return;
    }
    const response = await fetch(`${gameDetailUrl}?page=${currentPage}&limit=5`, {
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
    const paginate_data = invites_res.pagination;
    const totalPages = paginate_data.total_pages;
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
            const response = await fetch(joinUrl + "?room=" + invite.room_id, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`,
                }
            });
            response.json().then((data) => {
                if (!response.ok) {
                    alert(data.error);
                } else {
                    alert("Joined game successfully");
                    localStorage.setItem("game_id", data.data.game_id);
                    navigateTo("/game");
                }
            });
        });
    });
    goPagination(totalPages, currentPage, async (newPage) => {
        currentPage = newPage;
        fetchJoin();
    }, "pagination-container");
}
