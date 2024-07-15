import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, toggleHidden } from "../../utils/utils.js";

const resetUrlBase = "http://localhost:8004/user/pwd/change";

export async function fetchResetpassword() {
	document.querySelector('form').addEventListener('submit', async function(event) {
		event.preventDefault();

		const urlParams = new URLSearchParams(window.location.search);
		const uidb64 = urlParams.get("uidb64");
		const token = urlParams.get("token");
		const resetUrl = `${resetUrlBase}/${uidb64}/${token}/`;

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
		}

		try {
			const response = await fetch(resetUrl, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(body),
			});

			if (!response.ok) {
				const err = await response.json();
				throw err;
			}

			const data = await response.json();
			setTimeout(() => {
				navigateTo("/login");
			}, 2000);

		} catch (err) {
			if (err.error) {
				insertIntoElement('fields-warning', "Error: " + err.error);

			} else if (err.new_password) {
				insertIntoElement('fields-warning', "Password error: " + err.new_password[0]);
			} 
		}
	});
}

