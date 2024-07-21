import { navigateTo } from "../../utils/navTo.js";
import { userStatuses, RefreshToken, goPagination } from "../../utils/utils.js";
import { friendList, friendDelete, singleUserDetailUrl, pictureUrl } from "../../constants/constants.js";

let currentPage = 1;
let total_pages = 1;

export async function fetchFriends() {
    if (!localStorage.getItem("access_token")) {

        navigateTo("/login");
        return;
    }

    try {
        const response = await fetch(friendList + "?page=" + currentPage + "&limit=5", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            if (errorData.error === 'Token has expired') {
                await RefreshToken();
                return fetchFriends(); // Retry fetching after token refresh
            } else {
                throw new Error(errorData.error);
            }
        }

        const data = await response.json();
        const users = data.data;
        const paginate_data = data.pagination;
        if (paginate_data) {
            total_pages = paginate_data.total_pages;
        }

        const tableBody = document.querySelector('.widget-26 tbody');
        tableBody.innerHTML = ''; // Clear previous content

        if (users) {
            users.forEach(user => {
                fetch(singleUserDetailUrl + "?id=" + user.id, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                    }
                }).then(response => {
                    if (!response.ok) {
                        throw new Error("Failed to fetch user details");
                    }
                    return response.json();
                }).then(data => {
                    let user_res = data.data[0];

                    const userElement = document.createElement('tr');
                    let image = pictureUrl + "?id=" + user.id;
                    const user_status = userStatuses.includes(user.id);
                    userElement.innerHTML = `
                        <td>
                            <div class="widget-26-job-emp-img">
                                <img src="${image}" alt="User Image" />
                            </div>
                        </td>
                        <td>
                            <div class="widget-26-job-title">
                                <a data-nav href="/otherprofile?id=${user_res.id}">${user_res.username}</a>
                                <p class="m-0"><a data-nav href="#" class="employer-name">${user_res.first_name} ${user_res.last_name}</a></p>
                            </div>
                        </td>
                        <td>
                            <div class="widget-26-job-salary">ID: ${user_res.id}</div>
                        </td>
                        <td>
                            <div class="widget-26-job-category ${user_status ? 'bg-soft-success' : 'bg-soft-danger'}">
                                <i class="indicator ${user_status ? 'bg-success' : 'bg-danger'}"></i>
                                <span>${user_status ? 'Online' : 'Offline'}</span>
                            </div>
                        </td>
                        <td>
                            <div class="widget-26-job-starred">
                                <button id="delete-friend-button-${user_res.id}">Delete Friend</button>
                            </div>
                        </td>
                    `;

                    tableBody.appendChild(userElement);

                    document.getElementById(`delete-friend-button-${user_res.id}`).addEventListener("click", function(event) {
                        event.preventDefault();
                        deleteUser(user_res.id);
                    });

                }).catch((error) => {
                    console.error(error);
                    if (error.message === 'Token has expired') {
                        RefreshToken().then(() => {
                            fetchFriends();
                        });
                    } else {
                        alert(error.message);
                    }
                });
            });

            goPagination(total_pages, currentPage, async (newPage) => {
                currentPage = newPage;
                fetchFriends();
            }, "pagination-container");
        }
    } catch (error) {
        console.error(error);
        if (error.message === 'Token has expired') {
            await RefreshToken();
            return fetchFriends(); // Retry fetching after token refresh
        } else {
            alert(error.message);
        }
    }
}

async function deleteUser(userId) {
    try {
        const response = await fetch(friendDelete, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("access_token")}`
            },
            body: JSON.stringify({
                receiver_id: userId
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            if (errorData.error === 'Token has expired') {
                await RefreshToken();
                return deleteUser(userId); // Retry deleting after token refresh
            } else {
                throw new Error(errorData.error);
            }
        }

        await response.json();
        navigateTo("/friends");
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}





