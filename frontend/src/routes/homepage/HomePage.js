import { navigateTo } from "../../utils/navTo.js";



export async function fetchHomePage() {
    if (!localStorage.getItem("access_token")) {
        navigateTo("/login");
    }
}

