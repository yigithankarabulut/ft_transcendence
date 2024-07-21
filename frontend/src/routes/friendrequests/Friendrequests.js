import { navigateTo } from "../../utils/navTo.js";
import { goPagination, RefreshToken } from "../../utils/utils.js";
import { userGetByIdUrl, userDetailUrl, requestsList, acceptUrl, rejectUrl } from "../../contants/contants.js";

let currentPage = 1; // Current page
let total_pages = 1;

export async function fetchFriendrequests() {
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
            if (errorData.error === 'Token has expired') {
                console.log('Token expired, refreshing...');
                await RefreshToken();
                return fetchFriendrequests(); // Retry fetching after token refresh
            } else {
                throw new Error(errorData.error);
            }
        }
        const data = await response_user.json();
        const user = data.data[0];

        const response = await fetch(requestsList + "?page=" + currentPage + "&limit=5", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            }
        });
        if (!response.ok) {
            const errorData = await response.json();
            if (errorData.error === 'Token has expired') {
                console.log('Token expired, refreshing...');
                await RefreshToken();
                return fetchFriendrequests(); // Retry fetching after token refresh
            } else {
                throw new Error(errorData.error);
            }
        }

        const requests_res = await response.json();
        const requests = requests_res.data;
        let paginate_data = requests_res.pagination;
        if (paginate_data) {
            total_pages = paginate_data.total_pages;
        }

        console.log(requests);
        const tbody = document.querySelector(".table tbody");
        tbody.innerHTML = "";
        if (requests) {
            requests.forEach((request, index) => {
                fetch(userGetByIdUrl + "?id=" + request.id, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
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
                    sender_td.innerText = sender.username;
                    row.appendChild(sender_td);

                    const full_name = document.createElement("td");
                    full_name.innerText = sender.first_name + " " + sender.last_name;
                    row.appendChild(full_name);

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
                            const postAccept = (request_id) => {
                                return fetch(acceptUrl, {
                                    method: "POST",
                                    headers: {
                                        "Content-Type": "application/json",
                                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                                    },
                                    body: JSON.stringify({
                                        "receiver_id": request_id,
                                    })
                                });
                            };

                            const handleResponse = response => {
                                if (!response.ok) {
                                    return response.json().then(errorData => {
                                        if (response.status === 401 && errorData.error === "Token has expired") {
                                            return RefreshToken().then(() => {
                                                return postAccept(request.id).then(handleResponse);
                                            });
                                        } else {
                                            throw new Error(errorData.error);
                                        }
                                    });
                                } else {
                                    return response.json();
                                }
                            };
                            postAccept(request.id)
                                .then(handleResponse)
                                .then(() => {
                                    navigateTo("/friendrequests");
                                });
                        } catch (error) {
                            alert(error.message);
                        }
                    });

                    rejectButton.addEventListener("click", () => {
                        const data = {
                            "receiver_id": request.id,
                        };

                        const postRejectRequest = () => {
                            return fetch(rejectUrl, {
                                method: "DELETE",
                                headers: {
                                    "Content-Type": "application/json",
                                    "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                                },
                                body: JSON.stringify(data),
                            });
                        };

                        const handleResponse = response => {
                            if (!response.ok) {
                                return response.json().then(errorData => {
                                    if (response.status === 401 && errorData.error === "Token has expired") {
                                        return RefreshToken().then(() => {
                                            return postRejectRequest().then(handleResponse);
                                        });
                                    } else {
                                        throw new Error(errorData.error);
                                    }
                                });
                            }
                            return response.json();
                        };

                        postRejectRequest()
                            .then(handleResponse)
                            .then(() => {
                                navigateTo("/friendrequests");
                            })
                            .catch(error => {
                                alert(error.message);
                            });
                    });

                }).catch((error) => {
                    console.error(error);
                });
            });
            goPagination(total_pages, currentPage, async (newPage) => {
                currentPage = newPage;
                fetchFriendrequests();
            }, "pagination-container");
        }
    } catch (error) {
        console.error(error);
        if (error.message === 'Token has expired') {
            console.log('Token expired, refreshing...');
            await RefreshToken();
            return fetchFriendrequests(); // Retry fetching after token refresh
        } else {
            alert(error.message);
        }
    }
}
