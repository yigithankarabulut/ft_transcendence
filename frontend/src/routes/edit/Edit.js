import { navigateTo } from "../../utils/navTo.js";


const userDetailUrl = "http://127.0.0.1:8000/user/details";
const updateUserUrl = "http://127.0.0.1:8000/user/update";



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
        console.log(user);
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
                    throw new Error(errorData.error);
                }
                navigateTo("/profile");
            } catch (err) {
                console.log(err);
            }
        });
    } catch (err) {
        console.log(err);
    }
}
