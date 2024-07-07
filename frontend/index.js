

import { onlineStatus } from "./src/utils/utils.js";

import { navigateTo, router as originalRouter } from "./src/utils/navTo.js";

window.addEventListener("popstate", async () => {
    await customRouter();
});

function generateFavIcon() {
    let link = "public/images/42_Logo.svg.png";
    let faviconLinkElement = document.querySelector("link[rel~='icon']");
    faviconLinkElement.href = link;
}
generateFavIcon();

document.addEventListener("DOMContentLoaded", async () => {
    document.body.addEventListener("click", async (e) => {
        if (e.target.matches("[data-nav]")) {
            e.preventDefault();
            navigateTo(e.target.href);
            await customRouter();
        } else if (e.target.id === "logout-button") {
            e.preventDefault();
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('email');
            navigateTo('/login');
            await customRouter();
        }
    });

    await onlineStatus().catch(err => console.error("WebSocket connection error:", err));
    await customRouter().catch(err => console.error("Router error:", err)); // Improved error handling
});

async function customRouter() {
    await originalRouter();
    await onlineStatus().catch(err => console.error("WebSocket connection error:", err));
}
