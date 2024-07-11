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

        const room_id = document.createElement("td");
        room_id.innerText = request.room_id; // Adjust based on actual user object
        row.appendChild(room_id);

        const accept_buttonTd = document.createElement("td");
        const accept_button = document.createElement("button");
        accept_button.type = "button";
        accept_button.className = "btn btn-primary";
        accept_button.id = "accept-button";
        accept_button.innerText = "Accept";
        accept_buttonTd.appendChild(accept_button);
        row.appendChild(buttonTd);

        const reject_buttonTd = document.createElement("td");
        const reject_button = document.createElement("button");
        reject_button.type = "button";
        reject_button.className = "btn btn-primary";
        reject_button.id = "reject-button";
        reject_button.innerText = "Reject";
        reject_buttonTd.appendChild(reject_button);

        const buttonTd = document.createElement("td");
        const button = document.createElement("button");
        button.type = "button";
        button.className = "btn btn-primary";
        button.id = "accept-button";
        button.innerText = "Accept";
        buttonTd.appendChild(button);
        row.appendChild(buttonTd);

        tbody.appendChild(row);

        document.getElementById("accept-button").addEventListener("click", async () => {
            const response = await fetch(acceptUrl, {
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
        document.getElementById("reject-button").addEventListener("click", async () => {
            const response = await fetch(rejectUrl, {
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
