import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/base/Home";
import About from "@/components/base/About";
import Login from "@/components/user/Login";

Vue.use(Router);

var routes = [
    {
        path: "/",
        name: "home",
        component: Home
    },
    {
        path: "/about",
        name: "about",
        component: About
    },
    {
        path: "/login",
        name: "login",
        component: Login
    }
];

export default new Router({
    mode: "history",
    routes
});