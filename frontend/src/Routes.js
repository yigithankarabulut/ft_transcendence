// import Register from "./routes/register/Register.js";
import Login from "./routes/login/Login.js";
// import Home from "./routes/homepage/Homepage.js";
import TwoFA from "./routes/2fa/TwoFA.js";

export const routes = [
    // {
    //     path:"/",
    //     htmlPath: "./src/routes/homepage/homepage.html",
    //     js: "/src/routes/homepage/jshomepage.js",
    //     component: Home,
    // },
    {
        path:"/login",
        htmlPath: "./src/routes/login/login.html",
        js: "/src/routes/login/LoginJS.js",
        component: Login,
    },
    {
        path:"/2fa",
        htmlPath: "./src/routes/2fa/2fa.html",
        js: "/src/routes/2fa/TwoFAJS.js",
        component: TwoFA,
    },
    // {
    //     path:"/register",
    //     htmlPath: "./src/routes/register/register.html",
    //     js: "/src/routes/register/jsregister.js",
    //     component: Register,
    // }
    // {
    //     path:"/profile",
    //     component: Profile
    // }
]
