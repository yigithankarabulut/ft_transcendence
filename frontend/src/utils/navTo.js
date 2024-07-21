
import { routes } from "../Routes.js";
import { ws } from "../routes/game/Game.js";

import { onlineStatus } from "./utils.js";

const route = {
    "/ai": "fetchAi",
    "/edit": "fetchEdit",
    "/friendrequests": "fetchFriendrequests",
    "/friends": "fetchFriends",
    "/game": "fetchGame",
    "/": "fetchHomePage",
    "/join": "fetchJoin",
    "/localgame": "fetchLocalgame",
    "/login": "fetchLogin",
    "/otherprofile": "fetchOtherprofile",
    "/profile": "fetchProfile",
    "/quickplay": "fetchQuickplay",
    "/register": "fetchRegister",
    "/2fa" : "fetch2FA",
    "/auth": "fetchAuth",
    "/users": "fetchUsers",
    "/localtournament": "fetchLocaltournament",
    "/forgot-password": "fetchForgotpassword",
    "/reset-password": "fetchResetpassword",
    "/change-password": "fetchChangepassword",
    "/uname": "fetchConflictusername",
    "/404": "fetchAoa",
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
        document.getElementById("nav-bar").style.display = "none";
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
    } catch (err) {
        console.error("Error while render/routing component:", err);
    }
}

export const navigateTo = (url) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
    }
    history.pushState(null, null, url);
    router().then(() => console.log("Navigated to:", url));
}


window.addEventListener('popstate', router);
window.addEventListener('DOMContentLoaded', router);

window.addEventListener('popstate', () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
    }
});
