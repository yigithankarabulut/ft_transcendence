import { navigateTo } from "../../utils/navTo.js";



export async function fetchHomePage() {
    if (!localStorage.getItem("access_token")) {
        console.log("No access token found");
        navigateTo("/login");
    } else {
        console.log("Access token found");
    }
}

