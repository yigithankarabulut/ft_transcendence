import { navigateTo } from "../../../../ft_transcendence/frontend/src/utils/navTo.js";
import { toggleHidden,  insertIntoElement } from "../../../../ft_transcendence/frontend/src/utils/utils.js";


const userDetailUrl = "http://127.0.0.1:8000/user/details";
// const validToken = "http://127.0.0.1:8000/auth/token/validate";
// const refreshToken1 = "http://127.0.0.1:8000/auth/token/refresh";

document.getElementById('nav-bar').style.display = 'flex';
console.log("asd1");
fetchUserDetails();


export async function fetchUserDetails() {
	try {
			const response = await fetch(userDetailUrl, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				"Authorization": `Bearer ${localStorage.getItem("token")}`,
			}
		});
		if (!response.ok) {
			const errorData = await response.json();
			throw new Error(errorData.error);
		}

		const data = await response.json();
		const user = data[0].data[0];
		const fullname = document.getElementById('fullname');
		const username = document.getElementById('username');
		const email = document.getElementById('email');
		const phone = document.getElementById('phone');

		console.log(user.fullname, user.username, user.email, user.phone);
		insertIntoElement('fullname', user.first_name + " " + user.last_name);
		insertIntoElement('username', user.username);
		insertIntoElement('email', user.email);
		insertIntoElement('phone', user.phone);
		insertIntoElement('Username', user.username);
	} catch (err) {
		console.log(err);
		if (err.error === "Unauthorized") {
			navigateTo("/login");
		} else if (err.error === "Token has expired") {
			navigateTo("/login");
		} else if (err.error) {
			console.error("Error: ", err.error);
		} else {
			console.error("Error: internal server error");
		}
	}

	
}

