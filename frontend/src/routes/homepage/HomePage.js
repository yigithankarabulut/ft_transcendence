import { navigateTo } from "../../utils/navTo.js";
import { toggleHidden } from "../../utils/utils";

document.getElementById('nav-bar').style.display = 'flex';

const access_token = localStorage.getItem("access_token");
if (!access_token) {
    console.log("No access token found");
    navigateTo("/login");
} else {
    console.log("Access token found");

    toggleHidden('home-spinner');

    const handleButtonClick = (event) => {
        event.preventDefault();
        console.log("Button clicked");
    };

    const quickPlayButton = document.getElementById("quickplay-btn");
    if (quickPlayButton) {
        quickPlayButton.addEventListener("click", handleButtonClick);
    }
}
