import { navigateTo } from "../../utils/navTo.js";
import { insertIntoElement } from "../../utils/utils.js";
import { userDetailUrl, updateUserUrl, pictureUrl, avatarUpdateUrl } from "../../contants/contants.js";

export async function fetchEdit() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        navigateTo("/login");
        return;
    }

    try {
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
        const user = data[0].data[0];

        document.getElementById("profile-pic").src = pictureUrl + "?id=" + user.id;


        document.getElementById("full-name").textContent = `${user.first_name} ${user.last_name}`;
        document.getElementById("user-name").textContent = user.username;
        document.querySelector("input[name='first-name']").value = user.first_name;
        document.querySelector("input[name='user-name']").value = user.username;
        document.querySelector("input[name='last-name']").value = user.last_name;
        document.querySelector("input[name='phone']").value = user.phone;

        document.getElementById("save-button").addEventListener("click", async () => {
            const access_token = localStorage.getItem("access_token");
            const userName = document.querySelector("input[name='user-name']").value;
            const firstName = document.querySelector("input[name='first-name']").value;
            const lastName = document.querySelector("input[name='last-name']").value;
            const phone = document.querySelector("input[name='phone']").value;
            const fields_warning = document.getElementById('fields-warning');

            let body = {
                first_name: firstName,
                last_name: lastName,
                phone: phone,
                username: userName,
                email: user.email,
            };

            try {
                const response = await fetch(updateUserUrl, {
                    method: "PUT",
                    headers: {
                        "Authorization": `Bearer ${access_token}`,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(body),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw errorData;
                }
                alert("Profile updated successfully");
                navigateTo("/profile");

                } catch (err) {
                    if (err.error) {
                        insertIntoElement('fields-warning', "Error: " + err.error);
                    } else if (err.username) {
                        insertIntoElement('fields-warning', "Username error: " + err.username);
                    } else if (err.phone) {
                        insertIntoElement('fields-warning', "Phone error: " + err.phone);
                    } else if (err.first_name) {
                        insertIntoElement('fields-warning', "First name error: " + err.first_name);
                    } else if (err.last_name) {
                        insertIntoElement('fields-warning', "Last name error: " + err.last_name);
                    } else {
                        insertIntoElement('fields-warning', "Error: internal server error");
                        console.log(err);
                    }
                }
        });

        document.getElementById("cancel-button").addEventListener("click", () => {
            navigateTo("/profile");
        });

        document.getElementById("reset-pass").addEventListener("click", () => {
            navigateTo("/change-password");
        });

        document.getElementById("update-avatar").addEventListener("click", async () => {
            const image = document.getElementById("avatar-image").files[0];
            const formData = new FormData();
            formData.append('image', image);

            try {
                const res = await fetch(avatarUpdateUrl, {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${access_token}`,
                    },
                    body: formData,
                });

                if (!res.ok) {
                    throw new Error("Couldn't update avatar");
                }
                const data = await res.json();
                console.log(data);
                navigateTo("/profile");
            } catch (err) {
                console.log(err);
            }
        });

    } catch (err) {
        console.log(err);
    }
}
