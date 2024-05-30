import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden, insertIntoElement } from "../../utils/utils.js";
const userDetailUrl = "http://127.0.0.1:8000/user/details";

fetchUserDetails();

export async function fetchUserDetails() {
    console.log("Fetching user details")
    const token = localStorage.getItem("access_token");
    if (!token) {
        navigateTo("/login");
        return;
    }
    console.log("Token: ", token);
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
        console.log("User: ", user)

        // Bilgileri sayfaya ekleme
        insertIntoElement('username', user.username);
        insertIntoElement('first_name', user.first_name);
        insertIntoElement('last_name', user.last_name);
        insertIntoElement('email', user.email);

        // Sayfayı göster
        toggleHidden('profile-item');


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
