import { navigateTo } from "../../utils/navTo.js";
import { userStatuses } from "../../utils/utils.js";

const searchUrl = "http://127.0.0.1:8000/user/search";
const friendAdd = "http://127.0.0.1:8000/friends/add";
const userDetailUrl = "http://127.0.0.1:8000/user/details";


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
        const currentUser = data[0].data[0];
        const currentUserId = currentUser.id;
        document.getElementById('search-form').addEventListener("submit", function(event) {
            event.preventDefault();
        });

        document.getElementById("search-button").addEventListener("click", async () => {
            const searchValue = document.getElementById("search").value;
            const response = await fetch(searchUrl + "?page=1" + "&limit=5" +"&key=" + searchValue, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`,
                }
            });
            const data = await response.json();
            const users = data[0].data;

            const tableBody = document.querySelector('.widget-26 tbody');
            tableBody.innerHTML = ''; // Clear previous content
            users.forEach(user => {
                const userElement = document.createElement('tr');
                let randomImage = "https://placeimg.com/640/480/people"; // Random image URL
                const user_status = userStatuses.includes(user.id) ? true : false;
                console.log(user_status);
                console.log(userStatuses);
                console.log(user.id);
                userElement.innerHTML = `
                    <td>
                        <div class="widget-26-job-emp-img">
                            <img src="${randomImage}" alt="User Image" />
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
                        <div class="widget-26-job-salary">ID: ${user.id}</div>
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
                            throw new Error("Failed to send friend request");
                        }
                        return response.json();
                    }
                    ).then(data => {
                        console.log(`Sending friend request from user with ID: ${currentUserId} to user with ID: ${user.id}`);
                    });
                });
            });
        });

    }
}





