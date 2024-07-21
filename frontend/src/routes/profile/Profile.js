import { navigateTo } from "../../utils/navTo.js";
import { goPagination, RefreshToken } from "../../utils/utils.js";
import { userDetailUrl, matchHistoryUrl, pictureUrl } from "../../constants/constants.js";

let currentPage = 1; // Current page
let total_pages = 1;

export async function fetchProfile() {
    if (!localStorage.getItem("access_token")) {
        navigateTo("/login");
        return;
    }
    try {
        const response_user = await fetch(userDetailUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            }
        });
        if (!response_user.ok) {
            const errorData = await response_user.json();
            throw new Error(errorData.error);
        }

        const data_user = await response_user.json();
        const user = data_user.data[0];
        document.getElementById("full-name").textContent = `${user.first_name} ${user.last_name}`;
        document.getElementById("user-name").textContent = user.username;
        document.getElementById("profile-first-name").textContent = user.first_name;
        document.getElementById("profile-last-name").textContent = user.last_name;
        document.getElementById("phone").textContent = user.phone;
        document.getElementById("email").textContent = user.email;
        if (localStorage.getItem("status")) {
            document.getElementById("profile-status").textContent = localStorage.getItem("status");
        }

        async function fetchMatches() {
            const matchResponse = await fetch(`${matchHistoryUrl}?username=${user.username}&page=${currentPage}&limit=3`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                }
            });

            if (!matchResponse.ok) {
                const errorData = await matchResponse.json();
                if (errorData.error === 'Token has expired') {
                    await RefreshToken();
                    return fetchMatches(); // Retry fetching matches after token refresh
                } else {
                    throw new Error(errorData.error);
                }
            }

            const matchData = await matchResponse.json();
            const matches = matchData.data;
            const stats = matchData.stats;
            const paginate_data = matchData.pagination;

            if (paginate_data) {
                total_pages = paginate_data.total_pages;
            }

            if (stats) {
                document.getElementById('total-games').textContent = stats.total_games;
                document.getElementById('win-count').textContent = stats.win_count;
                document.getElementById('lose-count').textContent = stats.lose_count;
            }

            document.getElementById("profile-pic").src = pictureUrl + "?id=" + user.id + "&timestamp=" + new Date().getTime();
            const matchTableBody = document.querySelector("#match-history-table tbody");
            matchTableBody.innerHTML = "";

            if (matches) {
                matches.forEach(match => {
                    const date = new Date(match.date).toLocaleString();
                    const row = document.createElement("tr");
                    row.innerHTML = `
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
                    `;
                    matchTableBody.appendChild(row);
                });
            }

            goPagination(total_pages, currentPage, async (newPage) => {
                currentPage = newPage;
                fetchMatches(); // Replace fetchProfile with fetchMatches
            }, "pagination-container");
        }
        fetchMatches();
    } catch (error) {
        console.error(error);
        if (error.message === 'Token expired') {
            await RefreshToken();
            fetchProfile();
        } else {
            throw error;
        }
    }
}

