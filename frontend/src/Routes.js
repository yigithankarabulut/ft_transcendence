import LoginComponent from "./components/LoginComponent.js"
import RegisterComponent from "./components/RegisterComponent.js"
import TwoFAComponent from "./components/TwoFAComponent.js"
import HomePageComponent from "./components/HomePageComponent.js"
import ProfileComponent from "./components/ProfileComponent.js"
import GameComponent from "./components/GameComponent.js"
import QuickplayComponent from "./components/QuickplayComponent.js"
import JoinComponent from "./components/JoinComponent.js"
import EditComponent from "./components/EditComponent.js"
import FriendsComponent from "./components/FriendsComponent.js"
import UsersComponent from "./components/UsersComponent.js"
import LocalgameComponent from "./components/LocalgameComponent.js"
import AiComponent from "./components/AiComponent.js"
import SearchComponent from "./components/SearchComponent.js"
import OtherprofileComponent from "./components/OtherprofileComponent.js"


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
        component: QuickplayComponent,
    },
    {
        path:"/join",
        htmlPath: "./src/routes/join/join.html",
        js: "/src/routes/join/Join.js",
        component: JoinComponent,
    },
    {
        path:"/edit",
        htmlPath: "./src/routes/edit/edit.html",
        js: "/src/routes/edit/Edit.js",
        component: EditComponent,
    },
    {
        path:"/friends",
        htmlPath: "./src/routes/friends/friends.html",
        js: "/src/routes/friends/Friends.js",
        component: FriendsComponent,
    },
    {
        path:"/users",
        htmlPath: "./src/routes/users/users.html",
        js: "/src/routes/users/Users.js",
        component: UsersComponent,
    },
    {
        path:"/localgame",
        htmlPath: "./src/routes/localgame/localgame.html",
        js: "/src/routes/localgame/Localgame.js",
        component: LocalgameComponent,
    },
    {
        path:"/ai",
        htmlPath: "./src/routes/ai/ai.html",
        js: "/src/routes/ai/Ai.js",
        component: AiComponent,
    },
    {
        path:"/search",
        htmlPath: "./src/routes/search/search.html",
        js: "/src/routes/search/Search.js",
        component: SearchComponent,
    },
    {
        path:"/otherprofile",
        htmlPath: "./src/routes/otherprofile/otherprofile.html",
        js: "/src/routes/otherprofile/Otherprofile.js",
        component: OtherprofileComponent,
    },
]
