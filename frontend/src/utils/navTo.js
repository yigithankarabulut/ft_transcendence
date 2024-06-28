import { routes } from "../Routes.js";

export const router = async () => {
    console.log(location.pathname)
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
    console.log(match);
    const root = document.getElementById('root');
    const component = new match.route.component(match.route.htmlPath);
    try {
        const html = await component.render();
        root.innerHTML = html;
        const module = await import(match.route.js);

        if (location.pathname === "/profile" && module.fetchProfile) {
            module.fetchProfile();
        }

    } catch (err) {
        console.log("An error occurred while rendering the component.");
    }
}

export const navigateTo = (url) => {
    history.pushState(null, null, url);
    router();
}

//window.addEventListener('popstate', router);
//window.addEventListener('DOMContentLoaded', router);