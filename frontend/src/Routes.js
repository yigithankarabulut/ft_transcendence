import Login from "./routes/login/Login.js";
import HomePage from "./routes/homepage/HomePage.js";
import TwoFA from "./routes/2fa/TwoFA.js";
import Register from "./routes/register/Register.js";

export const routes = [
    {
         path:"/",
         htmlPath: "./src/routes/homepage/homepage.html",
         js: "/src/routes/homepage/HomePageJS.js",
         component: HomePage,
    },
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
    {
         path:"/register",
         htmlPath: "./src/routes/register/register.html",
         js: "/src/routes/register/RegisterJS.js",
         component: Register,
    },
    // {
    //     path:"/profile",
    //     component: Profile
    // }
]
