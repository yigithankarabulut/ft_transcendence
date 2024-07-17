import { navigateTo } from "../../utils/navTo.js";
import { goPagination } from "../../utils/utils.js";


const userGetByIdUrl = "http://127.0.0.1:8000/user/get/id";
const userDetailUrl = "http://127.0.0.1:8000/user/details";
const requestsList = "http://127.0.0.1:8000/friends/request";
const acceptUrl = "http://127.0.0.1:8000/friends/accept";
const rejectUrl = "http://127.0.0.1:8000/friends/reject";

let currentPage = 1; // Current page

export async function fetchFriendrequests() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        navigateTo("/login");
        return;
    }
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
    const data = await response_user.json();
    const user = data[0].data[0];

    const response = await fetch(requestsList + "?page=" + currentPage + "&limit=5" , {
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

    const requests_res = await response.json();
    const requests = requests_res.data
    let pagination = requests_res.pagination;
    let totalPages = pagination.total_pages;


    console.log(requests);
    const tbody = document.querySelector(".table tbody");
    tbody.innerHTML = "";
    let sender = {};
    requests.forEach((request, index) => {

        fetch(userGetByIdUrl + "?id=" + request.id, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,
            }
        }).then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to get user");
                }
                return response.json();
            }).then((data) => {
                let sender = data.data[0];

                const row = document.createElement("tr");

                const th = document.createElement("th");
                th.scope = "row";
                th.innerText = index + 1;
                row.appendChild(th);

                const sender_td = document.createElement("td");
                sender_td.innerText = sender.username; // Adjust based on actual user object
                row.appendChild(sender_td);

                const full_name = document.createElement("td");
                full_name.innerText = sender.first_name + " " + sender.last_name; // Adjust based on actual user object
                row.appendChild(full_name);

                      //add two buttons accept and reject button to each row
        const td = document.createElement("td");
        const acceptButton = document.createElement("button");
        acceptButton.id = "accept-button";
        acceptButton.innerText = "Accept";
        acceptButton.className = "btn btn-primary";
        td.appendChild(acceptButton);

        const rejectButton = document.createElement("button");
        rejectButton.id = "reject-button";
        rejectButton.innerText = "Reject";
        rejectButton.className = "btn btn-danger";
        td.appendChild(rejectButton);

        row.appendChild(td);

        tbody.appendChild(row);

        acceptButton.addEventListener("click", async () => {
            try {
                const response = await fetch(acceptUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`,
                    },
                    body: JSON.stringify({
                        "receiver_id": request.id,
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error);
                }
                navigateTo("/friendrequests");
            } catch (error) {
                alert(error.message);
            }
        });

        rejectButton.addEventListener("click", async () => {
            try {
                const response = await fetch(rejectUrl, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${access_token}`,
                    },
                    body: JSON.stringify({
                        "receiver_id": request.id,
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error);
                }
                navigateTo("/friendrequests");
            } catch (error) {
                alert(error.message);
            }
        });

            }).catch((error) => {
                console.error(error);
            });
    });
    goPagination(totalPages, currentPage, async (newPage) => {
        currentPage = newPage;
        fetchFriendrequests();
    }, "pagination-container");
}
