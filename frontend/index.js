
import { navigateTo, router } from "./src/utils/navTo.js";

window.addEventListener("popstate", router);

function generateFavIcon() {
    let link = "public/images/42_Logo.svg.png";
    let faviconLinkElement = document.querySelector("link[rel~='icon']");
    faviconLinkElement.href = link;
}
generateFavIcon();

document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", (e) => {
        if (e.target.matches("[data-nav]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        } else if (e.target.id === "logout-button") {
            logout();
        }
    });
    router().catch(err => console.error("Router error:", err)); // Improved error handling
});

function logout() {
    fetch('/logout', {
        method: 'POST',
        credentials: 'include'
    })
    .then(response => {
        if (response.ok) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('email');
            navigateTo('/login');
        } else {
            console.error('Logout failed');
        }
    })
    .catch(error => {
        console.error('Error during logout:', error);
    });
}
