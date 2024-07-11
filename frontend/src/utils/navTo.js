
import { routes } from "../Routes.js";

import { onlineStatus } from "./utils.js";

const route = {
    "/profile": "fetchProfile",
    "/quickplay": "fetchQuickplay",
    "/": "fetchHomePage",
    "/game": "fetchGame",
    "/join": "fetchJoin",
    "/edit": "fetchEdit",
    "/friends": "fetchFriends",
    "/users": "fetchUsers",
    "/localgame": "fetchLocalgame",
    "/ai": "fetchAi",
    "/auth": "fetchAuth",
    "/otherprofile": "fetchOtherprofile",
    // add more routes here.
};

export const router = async () => {
    const potentialMatches = routes.map(route => {
        return {
            route,
            isMatch: location.pathname === route.path
        }
    })
    let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch)
    if (!match) {
        match = {
            route: routes[0],
            isMatch: true
        }
    }

    await onlineStatus();
    const root = document.getElementById('root');
    const component = new match.route.component(match.route.htmlPath);
    try {
        root.innerHTML = await component.render();
        const module = await import(match.route.js);

        const routeFunction = route[location.pathname];
        if (routeFunction && module[routeFunction]) {
            module[routeFunction]();
        }
        await onlineStatus().catch(err => console.error("WebSocket connection error:", err));
    } catch (err) {
        console.log("Error while render/routing component:", err);
    }
}

export const navigateTo = (url) => {
    history.pushState(null, null, url);
    router().then(() => console.log("Navigated to:", url));
}


window.addEventListener('popstate', router);
window.addEventListener('DOMContentLoaded', router);
