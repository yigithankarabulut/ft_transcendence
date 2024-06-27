import LoginComponent from "./components/LoginComponent.js"
import RegisterComponent from "./components/RegisterComponent.js"
import TwoFAComponent from "./components/TwoFAComponent.js"
import HomePageComponent from "./components/HomePageComponent.js"
import ProfileComponent from "./components/ProfileComponent.js"
import GameComponent from "./components/GameComponent.js"
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
        path:"/profile",
        htmlPath: "./src/routes/profile/profile.html",
        js: "/src/routes/profile/Profile.js",
        component: ProfileComponent,
    },
    {
       path:"/game",
       htmlPath: "./src/routes/game/game.html",
       js: "/src/routes/game/Game.js",
       component: GameComponent,
    },
    {
        path:"/quickplay",
        htmlPath: "./src/routes/quickplay/quickplay.html",
        js: "/src/routes/quickplay/Quickplay.js",
        component: GameComponent,
     }
    //{
    //    path:"/tournament",
    //    htmlPath: "./src/routes/tournament/tournament.html",
    //    js: "/src/routes/tournament/Tournament.js",
    //    component: TournamentComponent,
    //},
]
