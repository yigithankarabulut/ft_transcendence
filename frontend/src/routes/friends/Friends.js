import { navigateTo } from "../../utils/navTo.js";
import { userStatuses } from "../../utils/utils.js";
import { goPagination } from "../../utils/utils.js";
import { friendList, friendDelete, userDetailUrl, singleUserDetailUrl, pictureUrl } from "../../contants/contants.js";

let currentPage = 1;
export async function fetchFriends() {

    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        console.log("No access token found");
        navigateTo("/login");
        return;
    } else {
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
        const currentUser = data_user[0].data[0];
        const currentUserId = currentUser.id;

        const response = await fetch(friendList + "?page=" + currentPage + "&limit=5", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,
            }
        });
        const data = await response.json();

        const users = data.data;
        const pagination = data.pagination;
        const totalPages = pagination.total_pages;


        const tableBody = document.querySelector('.widget-26 tbody');
        tableBody.innerHTML = ''; // Clear previous content
        users.forEach(user => {
            let user_res = {};
            fetch(singleUserDetailUrl + "?id=" + user.id, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`,
                }
            }).then(response => {
                if (!response.ok) {
                    throw new Error("Failed to fetch user details");
                }
                return response.json();
            }).then(data => {
                user_res = data.data[0];

            const userElement = document.createElement('tr');
            let image = pictureUrl + "?id=" + user.id;
            const user_status = userStatuses.includes(user.id) ? true : false;
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
                    <div class="widget-26-job-info">
                        <p class="type m-0">Email: ${user_res.email}</p>
                        <p class="text-muted m-0">Phone: <span class="location">${user_res.phone}</span></p>
                    </div>
                </td>
                <td>
                    <div class="widget-26-job-salary">ID: ${user_res.id}</div>
                </td>
                <td>
                <div class="widget-26-job-category ${user_status === false ?  'bg-soft-danger' : 'bg-soft-success' }">
                        <i class="indicator ${user_status === false ?  ' bg-danger' : 'bg-success' }"></i>
                        <span>${user_status === true ? 'Online' : 'Offline' }</span>
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
                fetch(friendDelete,{
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${access_token}`
                    },
                    body: JSON.stringify({
                        receiver_id: user_res.id
                    })
                }).then(response => {
                    if (!response.ok) {
                        return response.json().then(error => {
                            throw new Error(error.error);
                        });
                    }
                    return response.json();
                }).then(data => {
                    navigateTo("/friends");
                }).catch(error => {
                    alert(error.message);
                });
            });
        });
        });
        goPagination(totalPages, currentPage, async (newPage) => {
            currentPage = newPage;
            fetchFriends();
        }, "pagination-container");
    }
}





