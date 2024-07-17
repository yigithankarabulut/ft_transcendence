import { navigateTo } from "../../utils/navTo.js";

const userDetailUrl = "http://127.0.0.1:8000/user/details";
const matchHistoryUrl = "http://127.0.0.1:8000/game/history";
const pictureUrl = "http://localhost:8014/bucket/image/serve";
const matchesPerPage = 3; // Number of matches per page
let matches = []; // Match history data
let currentPage = 1; // Current page

export async function fetchProfile() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
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
        const response = await fetch(`${matchHistoryUrl}?username=${user.username}&page=${currentPage}&limit=${matchesPerPage}`, {
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
        matches = data.data;
        let stats = data.stats;

        document.getElementById("profile-pic").src = pictureUrl + "?id=" + user.id;
        document.getElementById('total-games').textContent = stats.total_games;
        document.getElementById('win-count').textContent = stats.win_count;
        document.getElementById('lose-count').textContent = stats.lose_count;

        const matchTableBody = document.querySelector("#match-history-table tbody");
        matchTableBody.innerHTML = "";

        // Calculate start and end indices for the current page
        const startIndex = (currentPage - 1) * matchesPerPage;
        const endIndex = Math.min(startIndex + matchesPerPage, matches.length);
        // Render match rows
        for (let i = startIndex; i < endIndex; i++) {
            const match = matches[i];
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
        }

        // Render pagination
        const totalPages = Math.ceil(matches.length / matchesPerPage);
        createPagination(totalPages, currentPage, async (newPage) => {
            currentPage = newPage;
            fetchProfile();
        }, "pagination-container");
}

//  bana yukardaki pagination stratejisini dinamik bir şekilde yapan başka page de kullanabileceğim bir fonksiyon yazın
//  ve bu fonksiyonu kullanarak aşağıdaki pagination fonksiyonunu refactor edin

function createPagination(totalPages, currentPage, onClick, elementId) {
    const paginationContainer = document.getElementById(elementId);
    paginationContainer.innerHTML = "";

    // Create previous button
    const prevButton = document.createElement("li");
    prevButton.innerHTML = `<li class="page-item ${currentPage === 1 ? "disabled" : ""}"><a href="#" class="page-link">&laquo;</a></li>`;
    prevButton.addEventListener("click", async (event) => {
        event.preventDefault();
        if (currentPage > 1) {
            currentPage--;
            onClick(currentPage);
        }
    });
    paginationContainer.appendChild(prevButton);

    // Create page number buttons
    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement("li");
        pageButton.innerHTML = `<li class="page-item ${i === currentPage ? "active" : ""}"><a href="#" class="page-link">${i}</a></li>`;
        pageButton.addEventListener("click", async (event) => {
            event.preventDefault();
            onClick(i);
        });
        paginationContainer.appendChild(pageButton);
    }

    // Create next button
    const nextButton = document.createElement("li");
    nextButton.innerHTML = `<li class="page-item ${currentPage === totalPages ? "disabled" : ""}"><a href="#" class="page-link">&raquo;</a></li>`;
    nextButton.addEventListener("click", async (event) => {
        event.preventDefault();
        if (currentPage < totalPages) {
            currentPage++;
            onClick(currentPage);
        }
    });
    paginationContainer.appendChild(nextButton);
}