import { navigateTo, router } from "./src/utils/navTo.js";
import { socketInstance } from "./src/socket/BaseSocket.js";



window.addEventListener("popstate", router);

function generateFavIcon() {
    let link = "public/images/42_Logo.svg.png";
    let faviconLinkElement = document.querySelector("link[rel~='icon']");
    faviconLinkElement.href = link;
}
generateFavIcon();

document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", (e) => {
        console.log(e);
        if (e.target.matches("a.nav-link")) {
            e.preventDefault();
            console.log(e.target.href)
            navigateTo(e.target.href);
        }
    })

    router();
})
