import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement } from "../../utils/utils.js";

const changeUrlBase = "http://localhost:8000/user/pwd/update";

export async function fetchChangepassword() {
	const access_token = localStorage.getItem("access_token");
	if (!access_token) {
		console.log("No access token found");
		navigateTo("/login");
	}else
	{
	document.querySelector('form').addEventListener('submit', async function(event) {
		event.preventDefault();

		const currentPassword = document.getElementById('current-password').value;
		const newPassword = document.getElementById('new-password').value;
		const confirmPassword = document.getElementById('confirm-password').value;
		const fields_warning = document.getElementById('fields-warning');
		const fields_success = document.getElementById('fields-success');

		if (newPassword === '' || confirmPassword === '') {
			insertIntoElement('fields-warning', "Fields shouldn't be empty");
			return;
		}

		if (newPassword !== confirmPassword) {
			insertIntoElement('fields-warning', 'New password and confirmed password do not match');
			return;
		}

		let body = {
			"new_password": newPassword,
			"old_password": currentPassword,
		}

		try {
			const response = await fetch(changeUrlBase, {
				method: 'POST',
				headers: {
					"Content-Type": "application/json",
					"Authorization": `Bearer ${access_token}`,
				},
				body: JSON.stringify(body),
			});

			if (!response.ok) {
				const err = await response.json();
				throw err;
			}

			const data = await response.json();
			setTimeout(() => {
				alert("Password changed successfully");
				navigateTo("/");
			}, 500);

		} catch (err) {
			if (err.error) {
				insertIntoElement('fields-warning', "Error: " + err.error);

			} else if (err.new_password) {
				insertIntoElement('fields-warning', "Password error: " + err.new_password[0]);
			}
		}
	});
}
}

