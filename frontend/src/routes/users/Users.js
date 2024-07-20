import { navigateTo } from "../../utils/navTo.js";
import { userStatuses } from "../../utils/utils.js";
import { goPagination } from "../../utils/utils.js";
import { searchUrl, friendAdd, userDetailUrl, pictureUrl } from "../../contants/contants.js";

let currentPage = 1; // Current page

export async function fetchUsers() {

    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        console.log("No access token found");
        navigateTo("/login");
    } else {
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
        const currentUser = data.data[0];
        const currentUserId = currentUser.id;
        document.getElementById('search-form').addEventListener("submit", function(event) {
            event.preventDefault();
        });

        document.getElementById("search-button").addEventListener("click", async () => {
            const searchValue = document.getElementById("search").value;
            const response = await fetch(searchUrl + "?page=" + currentPage + "&limit=5" +"&key=" + searchValue, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`,
                }
            });
            const data = await response.json();
            const users = data.data;

            let paginate_data = data.pagination;
            let totalPages = paginate_data.total_pages;

            const tableBody = document.querySelector('.widget-26 tbody');
            tableBody.innerHTML = ''; // Clear previous content
            users.forEach(user => {
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
                            <a data-nav href="/otherprofile?id=${user.id}">${user.username}</a>
                            <p class="m-0"><a data-nav href="#" class="employer-name">${user.first_name} ${user.last_name}</a></p>
                        </div>
                    </td>
                    <td>
                        <div class="widget-26-job-info">
                            <p class="type m-0">Email: ${user.email}</p>
                            <p class="text-muted m-0">Phone: <span class="location">${user.phone}</span></p>
                        </div>
                    </td>
                    <td>
                    <div class="widget-26-job-category ${user_status === false ?  'bg-soft-danger' : 'bg-soft-success' }">
                            <i class="indicator ${user_status === false ?  ' bg-danger' : 'bg-success' }"></i>
                            <span>${user_status === true ? 'Online' : 'Offline' }</span>
                        </div>
                    </td>
                    <td>
                        <div class="widget-26-job-starred">
                            <button id="add-friend-button-${user.id}">Add Friend</button>
                        </div>
                    </td>
                `;
                tableBody.appendChild(userElement);
                document.getElementById(`add-friend-button-${user.id}`).addEventListener("click", function(event) {
                    event.preventDefault();
                    fetch(friendAdd,{
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${access_token}`
                        },
                        body: JSON.stringify({
                            receiver_id: user.id
                        })
                    }).then(response => {
                        if (!response.ok) {
                            return response.json().then(error => {
                                // If the error message is "Cannot add yourself as a friend", throw an error
                                    throw new Error(error.error);
                            });
                        }
                        return response.json();
                    }).then(data => {
                        navigateTo("/users");
                    }).catch(error => {
                        // If an error was thrown, display an alert with the error message
                        alert(error.message);
                    });
                });
            });
            goPagination(totalPages, currentPage, async (newPage) => {
                currentPage = newPage;
                fetchUsers();
            }, "pagination-container");
        });

    }


}


