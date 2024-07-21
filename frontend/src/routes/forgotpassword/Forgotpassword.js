import { forgotpasswordUrl } from "../../constants/constants.js";

export async function fetchForgotpassword() {
	document.querySelector('form').addEventListener('submit', async function(event) {
		event.preventDefault();

		const email = document.getElementById('email').value;

		try {
			const response = await fetch(forgotpasswordUrl, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ email: email }),
			});

			if (!response.ok) {
				const error = await response.json();
				throw new Error(error.error);
			}

			alert('Password reset link has been sent to your email');
			window.location.href = "/login"; // Navigate to login page
		} catch (error) {
			alert(error.message);
		}
	});
}
