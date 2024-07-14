import { navigateTo } from "../../utils/navTo.js";
const userDetailUrl = "http://127.0.0.1:8000/user/details";
const requestsList = "http://127.0.0.1:8000/friends/request";
const acceptUrl = "http://127.0.0.1:8000/friends/accept";
const rejectUrl = "http://127.0.0.1:8000/friends/reject";


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



    const response = await fetch(requestsList + "?page=1&limit=10" , {
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

    // mimick data
    // const requests = [
    //     {
    //         "id": 1,
    //         "username": "user1",
    //         "first_name": "first_name1",
    //     },
    //     {
    //         "id": 2,
    //         "username": "user2",
    //         "first_name": "first_name2",
    //     },
    //     {
    //         "id": 3,
    //         "username": "user3",
    //         "first_name": "first_name3",
    //     }];

    console.log(requests);
    const tbody = document.querySelector(".table tbody");
    tbody.innerHTML = ""; // Clear existing rows

    requests.forEach((request, index) => {
        const row = document.createElement("tr");

        const th = document.createElement("th");
        th.scope = "row";
        th.innerText = index + 1;
        row.appendChild(th);

        const sender = document.createElement("td");
        sender.innerText = request.username; // Adjust based on actual user object
        row.appendChild(sender);

        const first_name = document.createElement("td");
        first_name.innerText = request.first_name; // Adjust based on actual user object
        row.appendChild(first_name);

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
            console.log("accept button clicked id:", user.id);
            await fetch(acceptUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`,
                },
                body: JSON.stringify({
                    "receiver_id": user.id,
                })
            });
        });

        rejectButton.addEventListener("click", async () => {
            console.log("reject button clicked id:", user.id);

            await fetch(rejectUrl, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`,
                },
                body: JSON.stringify({
                    "receiver_id": user.id,
                })
            });
        });
    });
}
