import { navigateTo } from "../../utils/navTo.js";
import { goPagination, CheckAuth } from "../../utils/utils.js";
import { userDetailUrl, matchHistoryUrl, pictureUrl } from "../../contants/contants.js";

let currentPage = 1; // Current page

export async function fetchProfile() {
    const access_token = localStorage.getItem("access_token");
    if (await CheckAuth() === false) {
        console.log(11111111111111111);
        navigateTo("/login");
        return;
    } else {
        console.log("Fetching user details");
        const response_user = await fetch(userDetailUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,
            }
        });
        if (!response_user.ok) {
            const errorData = await response_user.json();
            throw new Error(errorData.error);
        }

        const data_user = await response_user.json();
        const user = data_user[0].data[0];
        console.log("User Data:", user);

        document.getElementById("full-name").textContent = `${user.first_name} ${user.last_name}`;
        document.getElementById("user-name").textContent = user.username;
        document.getElementById("profile-first-name").textContent = user.first_name;
        document.getElementById("profile-last-name").textContent = user.last_name;
        document.getElementById("phone").textContent = user.phone;

        if (localStorage.getItem("status")) {
            document.getElementById("profile-status").textContent = localStorage.getItem("status");
        }

        console.log("Fetching match history");
        const response = await fetch(`${matchHistoryUrl}?username=${user.username}&page=${currentPage}&limit=3`, {
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
        const data = await response.json();
        let matches = data.data;
        let pagination = data.pagination;
        let totalPages = pagination.total_pages;
        let stats = data.stats;


        document.getElementById("profile-pic").src = pictureUrl + "?id=" + user.id;
        document.getElementById('total-games').textContent = stats.total_games;
        document.getElementById('win-count').textContent = stats.win_count;
        document.getElementById('lose-count').textContent = stats.lose_count;

        const matchTableBody = document.querySelector("#match-history-table tbody");
        matchTableBody.innerHTML = "";


        matches.forEach(match => {

            const date = new Date(match.date).toLocaleString();
            const row = document.createElement("tr");
            row.innerHTML = `
                <tr>
                    <td>
                        <h6 class="h5 mb-0 text-black">${date}</h6>
                        <hr>
                        <div class="row">
                            <div class="col-md-4 col-lg-4 mb-4 mb-lg-0">
                                <div class="text-center text-lg-left">
                                    <div class="d-block d-lg-flex align-items-center">
                                        <div class="text">
                                            <h3 class="h5 mb-0 text-black">${match.player1}</h3>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 col-lg-4 text-center mb-4 mb-lg-0">
                                <div class="d-inline-block">
                                    <div class="bg-black py-2 px-4 mb-2 text-white d-inline-block rounded">
                                        <span class="h5">${match.player1_score}:${match.player2_score}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 col-lg-4 mb-4 mb-lg-0">
                                <div class="text-center text-lg-right">
                                    <div class="d-block d-lg-flex align-items-center">
                                        <div class="text">
                                            <h3 class="h5 mb-0 text-black">${match.player2}</h3>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
            `;
            matchTableBody.appendChild(row);
        });
    goPagination(totalPages, currentPage, async (newPage) => {
        currentPage = newPage;
        fetchProfile();
    }, "pagination-container");
    }

}
