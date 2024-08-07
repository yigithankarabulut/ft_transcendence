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
import FriendrequestsComponent from "./components/FriendrequestsComponent.js"
import LocaltournamentComponent from "./components/LocaltournamentComponent.js"
import ForgotpasswordComponent from "./components/ForgotpasswordComponent.js"
import ResetpasswordComponent from "./components/ResetpasswordComponent.js"
import ChangepasswordComponent from "./components/ChangepasswordComponent.js"
import ConflictusernameComponent from "./components/ConflictusernameComponent.js"
import AoaComponent from "./components/AoaComponent.js"
import AuthComponent from "./components/AuthComponent.js"

export const routes = [
    {
        path:"/404",
        htmlPath: "./src/routes/aoa/aoa.html",
        js: "/src/routes/aoa/Aoa.js",
        component: AoaComponent,
    },
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
    {
        path:"/friendrequests",
        htmlPath: "./src/routes/friendrequests/friendrequests.html",
        js: "/src/routes/friendrequests/Friendrequests.js",
        component: FriendrequestsComponent,
    },
    {
        path:"/localtournament",
        htmlPath: "./src/routes/localtournament/localtournament.html",
        js: "/src/routes/localtournament/Localtournament.js",
        component: LocaltournamentComponent,
    },
    {
        path:"/forgot-password",
        htmlPath: "./src/routes/forgotpassword/forgotpassword.html",
        js: "/src/routes/forgotpassword/Forgotpassword.js",
        component: ForgotpasswordComponent,
    },
    {
        path:"/reset-password",
        htmlPath: "./src/routes/resetpassword/resetpassword.html",
        js: "/src/routes/resetpassword/Resetpassword.js",
        component: ResetpasswordComponent,
    },
    {
        path:"/change-password",
        htmlPath: "./src/routes/changepassword/changepassword.html",
        js: "/src/routes/changepassword/Changepassword.js",
        component: ChangepasswordComponent,
    },
    {
        path:"/uname",
        htmlPath: "./src/routes/conflictusername/conflictusername.html",
        js: "/src/routes/conflictusername/Conflictusername.js",
        component: ConflictusernameComponent,
    },
    {
        path:"/auth",
        htmlPath: "./src/routes/auth/auth.html",
        js: "/src/routes/auth/Auth.js",
        component: AuthComponent,
    }
]
