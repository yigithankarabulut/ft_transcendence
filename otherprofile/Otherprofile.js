import { navigateTo } from "../../utils/navTo.js";
import { userStatuses, goPagination } from "../../utils/utils.js";
import { userGetByIdUrl, matchHistoryUrl, pictureUrl } from "../../contants/contants.js";
const access_token = localStorage.getItem("access_token");

let currentPage = 1; // Current page


export async function fetchOtherprofile() {
    if (!access_token) {
        navigateTo("/login");
        return;
    }
    try {
        console.log("Fetching user details");
        const urlParams = new URLSearchParams(window.location.search);
        const id = urlParams.get('id');
        const user_status = userStatuses.includes(id) ? true : false;
        const userResponse = await fetch(userGetByIdUrl + "?id=" + id, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,
            }
        });
        if (!userResponse.ok) {
            const errorData = await userResponse.json();
            throw new Error(errorData.error);
        }
        const userData = await userResponse.json();
        const user = userData.data[0];
        console.log(user);

        document.getElementById("profile-pic").src = pictureUrl + "?id=" + user.id;
        document.getElementById("full-name").textContent = `${user.first_name} ${user.last_name}`;
        document.getElementById("user-name").textContent = user.username;
        document.getElementById("profile-first-name").textContent = user.first_name;
        document.getElementById("profile-last-name").textContent = user.last_name;
        document.getElementById("phone").textContent = user.phone;

        if (localStorage.getItem("status")) {
            document.getElementById("profile-status").textContent = localStorage.getItem("status");
        }

        console.log("Fetching match history");
        const matchResponse = await fetch(`${matchHistoryUrl}?username=${user.username}&page=${currentPage}&limit=3`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,
            }
        });
        if (!matchResponse.ok) {
            const errorData = await matchResponse.json();
            throw new Error(errorData.error);
        }
        const matchData = await matchResponse.json();
        const matches = matchData.data;
        const stats = matchData.stats;
        const paginate_data = matchData.pagination;
        const totalPages = paginate_data.total_pages;

        document.getElementById('total-games').textContent = stats.total_games;
        document.getElementById('win-count').textContent = stats.win_count;
        document.getElementById('lose-count').textContent = stats.lose_count;

        const matchTableBody = document.querySelector("#match-history-table tbody");
        matchTableBody.innerHTML = "";




        // Render match rows

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
        })

        goPagination(totalPages, currentPage, async (newPage) => {
            currentPage = newPage;
            fetchOtherProfile();
        }, "pagination-container");
    } catch (err) {
        console.log(err);
    }
}
