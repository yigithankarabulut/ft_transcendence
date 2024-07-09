import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden } from "../../utils/utils.js";


export async function fetchHomePage() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        console.log("No access token found");
        navigateTo("/login");
    } else {
        console.log("Access token found");
    }
}
