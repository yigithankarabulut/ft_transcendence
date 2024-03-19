import { navigateTo } from "../../../../ft_transcendence/frontend/src/utils/navTo.js";
import { toggleHidden,  insertIntoElement } from "../../../../ft_transcendence/frontend/src/utils/utils.js";


const url = "http://127.0.0.1:8000/user/update";

document.getElementById('nav-bar').style.display = 'flex';

// edit html id'si prfile-update olan button atacagi istek

document.getElementById('profile-update').addEventListener('click', (e) => {
	e.preventDefault();

	const first_name = document.getElementById('inputFirstName').value;
	const last_name = document.getElementById('inputLastName').value;
	const username = document.getElementById('inputUsername').value;
	const email = document.getElementById('inputEmailAddress').value;
	const phone = document.getElementById('inputPhone').value;
	console.log(first_name, last_name, username, email, phone);
	fetch(url, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json",
			"Authorization": `Bearer ${localStorage.getItem("token")}`,
		},
		body: JSON.stringify({
			"first_name": first_name,
			"last_name": last_name,
			"username": username,
			"email": email,
			"phone": phone,
		}),
	})
	.then(res => {
		if (!res.ok) {
			return res.json().then(err => {
				throw err;
			});
		}
		return res.json();
	})
	.then(data => {
			navigateTo("/profile");
	})
	.catch((err) => {
		if (err.error) {
			insertIntoElement('fields-warning', "Error: " + err.error);
		} else if (err.username) {
			insertIntoElement('fields-warning', "Error: " + err.username);
		} else if (err.email) {
			insertIntoElement('fields-warning', "Error: " + err.email);
		} else if (err.phone) {
			insertIntoElement('fields-warning', "Error: " + err.phone);
		} else {
			insertIntoElement('fields-warning', "Error: internal server error");
		}
		toggleHidden('profile-update');
	});
})
