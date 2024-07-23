import { navigateTo } from "../../utils/navTo.js";
import { userStatuses, RefreshToken, goPagination } from "../../utils/utils.js";
import { searchUrl, friendAdd, pictureUrl, friendRelationshipUrl } from "../../constants/constants.js";

let currentPage = 1;
let total_pages = 1;

export async function fetchUsers() {
    if (!localStorage.getItem("access_token")) {

        navigateTo("/login");
        return;
    }

    document.getElementById('search-form').addEventListener("submit", function(event) {
        event.preventDefault();
    });

    document.getElementById("search-button").addEventListener("click", async () => {
        const searchValue = document.getElementById("search").value;
        if (searchValue == "")
        return;
        await fetchUserSearch(searchValue);
    });

    async function fetchUserSearch(searchValue) {
        try {
            const response = await fetch(searchUrl + "?page=" + currentPage + "&limit=5" + "&key=" + searchValue, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                if (response.status === 401) {
                    if (errorData.error === 'Token has expired') {
                        await RefreshToken();
                        return fetchUserSearch(searchValue); // Retry fetching after token refresh
                    } else {
                        document.getElementById("logout-button").click();
                        return;
                    }
                }
                throw new Error(errorData.error);
            }

            const data = await response.json();
            const users = data.data;
            if (!users) {
                alert("No users found");
                return;
            }

            let paginate_data = data.pagination;
            if (paginate_data) {
                total_pages = paginate_data.total_pages;
            }

            const tableBody = document.querySelector('.widget-26 tbody');
            tableBody.innerHTML = '';
            const  postData = users.map(user => user.id);
            console.log(postData);
            const resp = await fetch(friendRelationshipUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                },
                body: JSON.stringify({players:postData})
            });
            if (!resp.ok)
            {
                if (resp.status === 401) {
                    if (errorData.error === 'Token has expired') {
                        await RefreshToken();
                        return fetchUserSearch(searchValue); // Retry fetching after token refresh
                    } else {
                        document.getElementById("logout-button").click();
                        return;
                    }
                }
                throw new Error(errorData.error);
            }

            const userRelations = await resp.json();
            if (users) {
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
                                <p class="m-0"><a data-nav href="otherprofile?id=${user.id}" class="employer-name">${user.first_name} ${user.last_name}</a></p>
                            </div>
                        </td>
                        <td>
                            <div class="widget-26-job-category ${user_status ? 'bg-soft-success' : 'bg-soft-danger'}">
                                <i class="indicator ${user_status ? 'bg-success' : 'bg-danger'}"></i>
                                <span>${user_status ? 'Online' : 'Offline'}</span>
                            </div>
                        </td>
                        <td>
                            <div class="widget-26-job-salary">${user.email}</div>
                        </td>
                    `;
                    if (userRelations.data[user.id] == 0) //pending
                    {
                        userElement.innerHTML += `
                            <td>
                                <div class="widget-26-job-starred" style="background-color:yellow; text-align:center; padding:5px; border-radius:15px;">
                                    Pending!
                                </div>
                            </td>
                        `;
                        tableBody.appendChild(userElement);
                    } else if (userRelations.data[user.id] == 1) //accepted
                    {
                        userElement.innerHTML += `
                        <td>
                            <div class="widget-26-job-starred" style="background-color:green; text-align:center; padding:5px; border-radius:15px;">
                                Friend!
                            </div>
                        </td>
                        `;
                        tableBody.appendChild(userElement);
                    } else if (userRelations.data[user.id] == 5) // non relationship
                    {
                        userElement.innerHTML += `
                            <td>
                            <div class="widget-26-job-starred">
                                <button id="add-friend-button-${user.id}">Add Friend</button>
                            </div>
                            </td>
                        `;
                        tableBody.appendChild(userElement);


                        document.getElementById(`add-friend-button-${user.id}`).addEventListener("click", function(event) {
                            event.preventDefault();
                            const button = document.getElementById(`add-friend-button-${user.id}`);
                            button.value = "Pending";
                            button.disabled = true;
                            button.style.backgroundColor = "yellow";
                            button.style.color = "black";
                            addUser(user.id);
                        });
                    }
                });
                goPagination(total_pages, currentPage, async (newPage) => {
                    currentPage = newPage;
                    fetchUserSearch(searchValue);
                }, "pagination-container");
            }
        } catch (error) {
            console.error(error);
            if (error.message === 'Token has expired') {
                await RefreshToken();
                return fetchUserSearch(searchValue); 
            } else {
                alert(error.message);
            }
        }
    }

    async function addUser(userId) {
        try {
            const response = await fetch(friendAdd, {
                method: 'POST',
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
                if (response.status === 401) {
                    if (errorData.error === 'Token has expired') {
                        await RefreshToken();
                        return addUser(userId); // Retry adding after token refresh
                    }
                    document.getElementById("logout-button").click();
                    return;
                }
                throw new Error(errorData.error);
            }

            await response.json();
            alert("Friend request sent successfully");
            navigateTo("/users");
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    }
}
