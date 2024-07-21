import { navigateTo } from "../../utils/navTo.js";
import { goPagination, RefreshToken } from "../../utils/utils.js";
import { gameDetailUrl, joinUrl } from "../../constants/constants.js";

let currentPage = 1; // Current page
let total_pages = 1;

export async function fetchJoin() {
    if (!localStorage.getItem("access_token")) {
        navigateTo("/login");
        return;
    }

    try {
        const response = await fetch(gameDetailUrl + "?page=" + currentPage + "&limit=5", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
                if (response.status === 401) {
                    if (errorData.error === 'Token has expired') {
                        await RefreshToken();
                        return fetchJoin(); // Retry fetching invites after token refresh
                    }
                    document.getElementById("logout-button").click();
                    return;
            }
            throw new Error(errorData.error);
        }

        const invites_res = await response.json();
        const invites = invites_res.data;
        const paginate_data = invites_res.pagination;
        if (paginate_data) {
            total_pages = paginate_data.total_pages;
        }

        const tbody = document.querySelector(".table tbody");
        tbody.innerHTML = ""; // Clear existing rows

        if (invites) {
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
                button.addEventListener("click", () => {
                    const postJoinRequest = () => {
                        return fetch(joinUrl + "?room=" + invite.room_id, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                            }
                        });
                    };

                    const handleResponse = response => {
                        if (!response.ok) {
                            return response.json().then(data => {
                                if (response.status === 401) {
                                    if (data.error === 'Token has expired') {
                                        return RefreshToken().then(() => {
                                            return postJoinRequest().then(handleResponse);
                                        });
                                    }
                                    document.getElementById("logout-button").click();
                                    return;
                                }
                                throw new Error(data.error);
                            });
                        }
                        return response.json();
                    };
                    postJoinRequest()
                        .then(handleResponse)
                        .then((data) => {
                            if (!data.error) {
                                alert("Joined game successfully");
                                localStorage.setItem("game_id", data.data.game_id);
                                navigateTo("/game");
                            }
                        })
                        .catch(error => {
                            alert(error.message);
                        });
                });
            });

            goPagination(total_pages, currentPage, async (newPage) => {
                currentPage = newPage;
                fetchJoin();
            }, "pagination-container");
        }
    } catch (error) {
        console.error(error);
        if (error.message === 'Token has expired') {
            await RefreshToken();
            return fetchJoin(); // Retry fetching invites after token refresh
        } else {
            alert(error.message);
        }
    }
}
