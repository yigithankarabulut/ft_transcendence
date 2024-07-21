import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, RefreshToken } from "../../utils/utils.js";
import { changeUrlBase } from "../../constants/constants.js"

export async function fetchChangepassword() {
	if (!localStorage.getItem("access_token")) {

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

		const postChangePasswordRequest = () => {
			return fetch(changeUrlBase, {
				method: 'POST',
				headers: {
					"Content-Type": "application/json",
					"Authorization": `Bearer ${localStorage.getItem("access_token")}`,
				},
				body: JSON.stringify(body),
			});
		};

		const handleResponse = response => {
			if (!response.ok) {
				return response.json().then(errorData => {
					if (response.status === 401 && errorData.error === "Token has expired") {
						return RefreshToken().then(() => {
							return postChangePasswordRequest().then(handleResponse);
						});
					} else if (response.status === 401 && errorData.error) {
						document.getElementById("logout-button").click();
					} else {
						throw errorData;
					}
				});
			}
			return response.json();
		};

		postChangePasswordRequest()
			.then(handleResponse)
			.then(data => {
				if (data.error) {
					insertIntoElement('fields-warning', "Error: " + data.error);
					return;
				}
				setTimeout(() => {
					alert("Password changed successfully");
					navigateTo("/");
				}, 500);
			})
			.catch(err => {
				if (err.error) {
					insertIntoElement('fields-warning', "Error: " + err.error);
				} else if (err.new_password) {
					insertIntoElement('fields-warning', "Password error: " + err.new_password[0]);
				}
			});
	});
}
}

