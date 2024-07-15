import { navigateTo } from "../../utils/navTo.js";

const resetUrlBase = "http://localhost:8004/user/pwd/change";

export async function fetchResetpassword() {
	document.querySelector('form').addEventListener('submit', async function(event) {
		event.preventDefault();

		const urlParams = new URLSearchParams(window.location.search);
		const uidb64 = urlParams.get("uidb64");
		const token = urlParams.get("token");
		const resetUrl = resetUrlBase + "/" + uidb64 + "/" + token + "/";

		const newPassword = document.getElementById('new-password').value;
		const confirmPassword = document.getElementById('confirm-password').value;

		if (newPassword !== confirmPassword) {
			alert('New password and confirmed password do not match');
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
				body: JSON.stringify(body)
			});

			if (!response.ok) {
				const error = await response.json();
				throw new Error(error.error);
			}

			alert('Password has been reset successfully');
			navigateTo("/login");
		} catch (error) {
			alert(error.message);
		}
	});
}
