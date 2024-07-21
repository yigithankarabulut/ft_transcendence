import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement, RefreshToken } from "../../utils/utils.js";
import { userDetailUrl, updateUserUrl, pictureUrl, avatarUpdateUrl } from "../../constants/constants.js";

export async function fetchEdit() {
    if (!localStorage.getItem("access_token")) {
        navigateTo("/login");
        return;
    }

    try {
        const response = await fetch(userDetailUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error);
        }

        const data = await response.json();
        const user = data.data[0];


        document.getElementById("profile-pic").src = pictureUrl + "?id=" + user.id + "&timestamp=" + new Date().getTime();
        document.getElementById("full-name").textContent = `${user.first_name} ${user.last_name}`;
        document.getElementById("user-name").textContent = user.username;
        document.querySelector("input[name='first-name']").value = user.first_name;
        document.querySelector("input[name='user-name']").value = user.username;
        document.querySelector("input[name='last-name']").value = user.last_name;
        document.querySelector("input[name='email']").value = user.email;

        document.getElementById("save-button").addEventListener("click", async () => {
            const userName = document.querySelector("input[name='user-name']").value;
            const firstName = document.querySelector("input[name='first-name']").value;
            const lastName = document.querySelector("input[name='last-name']").value;
            const email = document.querySelector("input[name='email']").value;
            const fields_warning = document.getElementById('fields-warning');

            let body = {
                first_name: firstName,
                last_name: lastName,
                username: userName,
                email: email,
            };

            const postUpdateUserRequest = () => {
                return fetch(updateUserUrl, {
                    method: 'PUT',
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
                                return postUpdateUserRequest().then(handleResponse);
                            });
                        } else if (response.status === 207) {
                            alert("Email updated successfully, please verify your email");
                            document.getElementById("logout-button").click();
                            return;
                        }
                        else {
                            throw errorData;
                        }
                    });
                }
                return response.json();
            };

            postUpdateUserRequest()
                .then(handleResponse)
                .then(() => {
                    alert("Profile updated successfully");
                    navigateTo("/profile");
                })
                .catch(err => {
                    if (err.error) {
                        insertIntoElement('fields-warning', "Error: " + err.error);
                    } else if (err.username) {
                        insertIntoElement('fields-warning', "Username error: " + err.username);
                    } else if (err.first_name) {
                        insertIntoElement('fields-warning', "First name error: " + err.first_name);
                    } else if (err.last_name) {
                        insertIntoElement('fields-warning', "Last name error: " + err.last_name);
                    } else if (err.email) {
                        insertIntoElement('fields-warning', "Email error: " + err.email);
                    } else {
                        insertIntoElement('fields-warning', "Error: internal server error");
                        console.error(err);
                    }
                });
        });

        document.getElementById("cancel-button").addEventListener("click", () => {
            navigateTo("/profile");
        });

        document.getElementById("reset-pass").addEventListener("click", () => {
            navigateTo("/change-password");
        });

        document.getElementById("update-avatar").addEventListener("click", async () => {
            const image = document.getElementById("avatar-image").files[0];
            if (!image)
            {
                alert("U need select image first!!");
                return;
            }
            const formData = new FormData();
            formData.append('image', image);

            const postAvatarUpdate =  () => {
                return fetch(avatarUpdateUrl, {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    body: formData,
                });
            };
            const handleResponse = response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        if (response.status === 401 && errorData.error === "Token has expired") {
                            return RefreshToken().then(() => {
                                return postAvatarUpdate().then(handleResponse);
                            });
                        } else {
                            throw new Error("Couldn't update avatar");
                        }
                    });
                }
                return response.json();
            };
            postAvatarUpdate()
                .then(handleResponse)
                .then(data => {
                    alert("Avatar updated successfully");
                    navigateTo("/profile");
                })
                .catch(error => {
                    console.error(error);
                });
        });

    } catch (err) {
        console.error(err);
    }
}
