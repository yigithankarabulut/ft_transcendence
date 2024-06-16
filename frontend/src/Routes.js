import LoginComponent from "./components/LoginComponent.js"
import RegisterComponent from "./components/RegisterComponent.js"
import TwoFAComponent from "./components/TwoFAComponent.js"
import HomePageComponent from "./components/HomePageComponent.js"
<<<<<<< HEAD
import ProfileComponent from "./components/ProfileComponent.js"
import SearchComponent     from "./components/SearchComponent.js"
import QuickplayComponent from "./components/QuickplayComponent.js"
=======
import FriendsComponent from "./components/FriendsComponent.js"
//import ProfileComponent from "./components/ProfileComponent.js"
>>>>>>> 59b054ba26e225d7bf23f3293763f09b791dd1a7
//import GameComponent from "./components/GameComponent.js"
//import TournamentComponent from "./components/TournamentComponent.js"


export const routes = [
    {
        path:"/",
        htmlPath: "./src/routes/homepage/homepage.html",
        js: "/src/routes/homepage/HomePage.js",
        component: HomePageComponent,
    },
    {
        path:"/login",
        htmlPath: "./src/routes/login/login.html",
        js: "/src/routes/login/Login.js",
        component: LoginComponent,
    },
    {
        path:"/2fa",
        htmlPath: "./src/routes/twofa/twofa.html",
        js: "/src/routes/twofa/TwoFA.js",
        component: TwoFAComponent,
    },
    {
        path:"/register",
        htmlPath: "./src/routes/register/register.html",
        js: "/src/routes/register/Register.js",
        component: RegisterComponent,
    },
    {
<<<<<<< HEAD
        path:"/profile",
        htmlPath: "./src/routes/profile/profile.html",
        js: "/src/routes/profile/Profile.js",
        component: ProfileComponent,
    },
    {
        path: "/search",
        htmlPath: "./src/routes/search/search.html",
        js: "/src/routes/search/Search.js",
        component: SearchComponent,
    },
    {
        path: "/quickplay",
        htmlPath: "./src/routes/quickplay/quickplay.html",
        js: "/src/routes/quickplay/Quickplay.js",
        component: QuickplayComponent,
=======
        path:"/friends",
        htmlPath: "./src/routes/friends/friends.html",
        js: "/src/routes/friends/Friends.js",
        component: FriendsComponent,
>>>>>>> 59b054ba26e225d7bf23f3293763f09b791dd1a7
    }


    //{
    //    path:"/game",
    //    htmlPath: "./src/routes/game/game.html",
    //    js: "/src/routes/game/Game.js",
    //    component: GameComponent,
    //},
    //{
    //    path:"/tournament",
    //    htmlPath: "./src/routes/tournament/tournament.html",
    //    js: "/src/routes/tournament/Tournament.js",
    //    component: TournamentComponent,
    //},
]
