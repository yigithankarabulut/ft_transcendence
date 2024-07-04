import { navigateTo } from "../../utils/navTo.js";
const userDetailUrl = "http://127.0.0.1:8000/user/details";

export async function fetchJoin() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        navigateTo("/login");
        return;
    }
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
    const users = data[0].data; // Assuming this is an array of users

    const tbody = document.querySelector(".table tbody");
    tbody.innerHTML = ""; // Clear existing rows

    users.forEach((user, index) => {
        const row = document.createElement("tr");

        const th = document.createElement("th");
        th.scope = "row";
        th.innerText = index + 1;
        row.appendChild(th);

        const firstNameTd = document.createElement("td");
        firstNameTd.innerText = user.first_name; // Adjust based on actual user object
        row.appendChild(firstNameTd);

        const lastNameTd = document.createElement("td");
        lastNameTd.innerText = user.last_name; // Adjust based on actual user object
        row.appendChild(lastNameTd);

        const buttonTd = document.createElement("td");
        const button = document.createElement("button");
        button.type = "button";
        button.className = "btn btn-primary";
        button.innerText = "Join";
        buttonTd.appendChild(button);
        row.appendChild(buttonTd);

        tbody.appendChild(row);

		button.addEventListener("click", async () => {
			// Perform join logic here
			console.log(`Joining user: ${user.first_name} ${user.last_name}`);
			localStorage.setItem("room_id", JSON.stringify(user.first_name));
			navigateTo("/game");
		});
    });
}
