
import { navigateTo} from "./src/utils/navTo.js";
import { socket } from "./src/utils/utils.js";



document.querySelector("link[rel~='icon']").href = "public/images/42_Logo.svg.png";

document.addEventListener("DOMContentLoaded", async () => {
    document.body.addEventListener("click", async (e) => {
        if (e.target.matches("[data-nav]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        } else if (e.target.id === "logout-button") {
            e.preventDefault();
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.close();
            }
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('email');
            navigateTo('/login');
            // window.location.reload();
        }
    });
});
