import { navigateTo } from "../../utils/route.js";
import { toggleHidden, insertIntoElement } from "../../utils/utils.js";

const userDetailUrl = "http://127.0.0.1:8000/user/details";

document.addEventListener("DOMContentLoaded", async () => {
    await fetchUserDetails();
});

async function fetchUserDetails() {
    const token = localStorage.getItem("token");
    if (!token) {
        navigateTo("/login");
        return;
    }
    try {
        const response = await fetch(userDetailUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error);
        }

        const data = await response.json();
        const user = data[0].data[0];

        // Bilgileri sayfaya ekleme
        const profileImageUrl = '../../../public/images/ykarabul.ico';
        document.getElementById('profile-image').src = profileImageUrl;
        insertIntoElement('username', user.username);
        insertIntoElement('first_name', user.first_name);
        insertIntoElement('last_name', user.last_name);
        insertIntoElement('email', user.email);

        toggleHidden('user-details');
    } catch (err) {
        console.log(err);
        if (err.message === "Unauthorized" || err.message === "Token has expired") {
            navigateTo("/login");
        } else if (err.message) {
            console.error("Error: ", err.message);
        } else {
            console.error("Error: internal server error");
        }
    }
}
