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
        }
    })
    router().catch(err => console.error("Router error:", err)); // Improved error handling
})
