import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden } from "../../utils/utils.js";

const userDetailUrl = "http://127.0.0.1:8000/user/details";
const updateUserUrl = "http://127.0.0.1:8000/user/update";
const matchHistoryUrl = "http://127.0.0.1:8000/game/history";
const access_token = localStorage.getItem("access_token");
const matchesPerPage = 3; // Number of matches per page
let matches = []; // Match history data
let currentPage = 1; // Current page
let originalUserData = {};

export async function fetchProfile() {
    if (!access_token) {
        navigateTo("/login");
        return;
    }
    try {
        console.log("Fetching user details");
        const response = await fetch(userDetailUrl, {
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
        const user = data[0].data[0];
        console.log(user);

        user.win_count = 654546;
        document.getElementById("full-name").textContent = `${user.first_name} ${user.last_name}`;
        document.getElementById("user-name").textContent = user.username;
        document.getElementById("profile-first-name").textContent = user.first_name;
        document.getElementById("profile-last-name").textContent = user.last_name;
        document.getElementById("phone").textContent = user.phone;

        document.getElementById("total-count").textContent = user.win_count + user.lose_count;
        document.getElementById("win-count").textContent = user.win_count;
        document.getElementById("lose-count").textContent = user.lose_count;


        if (localStorage.getItem("status")) {
            document.getElementById("profile-status").textContent = localStorage.getItem("status");
        }

        // match history
        await renderMatchHistory(user.username);

    } catch (err) {
        console.log(err);
    }

}

// Function to render match history table
async function renderMatchHistory(username) {
    try {
        console.log("Fetching match history");
        const response = await fetch(matchHistoryUrl + `?username=${username}&page=${currentPage}&limit=${matchesPerPage}`, {
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
        console.log("Match history data:");
        console.log(data.data);
        matches = data.data;

        console.log(matches);

        const matchTableBody = document.querySelector("#match-history-table tbody");
        matchTableBody.innerHTML = "";

        // Calculate start and end indices for the current page
        const startIndex = (currentPage - 1) * matchesPerPage;
        const endIndex = Math.min(startIndex + matchesPerPage, matches.length);

        // Render match rows
        for (let i = startIndex; i < endIndex; i++) {
            const match = matches[i];
            const row = document.createElement("tr");
            row.innerHTML = `
                <th>
                    <div class="col-md-4 col-lg-4 mb-4 mb-lg-0">
                        <div class="text-center text-lg-left">
                        <div class="d-block d-lg-flex align-items-center">
                            <div class="text">
                            <h3 class="h5 mb-0 text-black">${match.player1}</h3>
                            </div>
                        </div>
                        </div>
                    </div>
                </th>
                <div class="col-md-4 col-lg-4 text-center mb-4 mb-lg-0">
                    <div class="d-inline-block">
                        <div class="bg-black py-2 px-4 mb-2 text-white d-inline-block rounded">
                            <span class="h5">${match.player1_score}:${match.player2_score}</span>
                        </div>
                    </div>
                </div>
                <th>
                    <div class="col-md-4 col-lg-4 mb-4 mb-lg-0">
                        <div class="text-center text-lg-right">
                            <div class="d-block d-lg-flex align-items-center">
                                <div class="text">
                                    <h3 class="h5 mb-0 text-black">${match.player2}</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </th>
            `;
            matchTableBody.appendChild(row);
        }

         await renderPaginationControls();

    } catch (err) {
        console.log(err);
    }
}

// Function to render pagination controls
async function renderPaginationControls() {
    const paginationContainer = document.getElementById("pagination");
    paginationContainer.innerHTML = "";

    const totalPages = Math.ceil(matches.length / matchesPerPage);

    // Create previous button
    const prevButton = document.createElement("li");
    prevButton.innerHTML = `<li class="page-item disabled"><a href="#" class="page-link">&laquo;</a></li>`;
    prevButton.addEventListener("click", async () => {
        if (currentPage > 1) {
            currentPage--;
            await renderMatchHistory();
        }
    });
    paginationContainer.appendChild(prevButton);

    // Create page number buttons
    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement("li");
        pageButton.innerHTML = `<li class="page-item ${i === currentPage ? "active" : ""}"><a href="#" class="page-link">${i}</a></li>`;
        pageButton.addEventListener("click", async () => {
            currentPage = i;
            await renderMatchHistory();
        });
        paginationContainer.appendChild(pageButton);
    }

    // Create next button
    const nextButton = document.createElement("li");
    nextButton.innerHTML = `<li class="page-item disabled"><a href="#" class="page-link">&raquo;</a></li>`;
    nextButton.addEventListener("click", async () => {
        if (currentPage < totalPages) {
            currentPage++;
            await renderMatchHistory();
        }
    });
    paginationContainer.appendChild(nextButton);
}
