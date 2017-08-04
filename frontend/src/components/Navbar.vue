<template>
    <nav class="navbar container">
        <div class="navbar-brand">
            <router-link class="navbar-item" to="/">OpenCTF</router-link>
            <div class="navbar-burger" data-target="main-navbar">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        <div id="main-navbar" class="navbar-menu">
            <div class="navbar-start">
                <router-link class="navbar-item" to="/about">About</router-link>
            </div>
            <div class="navbar-end">
                <router-link class="navbar-item" v-show="!isLoggedIn()" to="/login">Login</router-link>
                <router-link class="navbar-item" v-show="!isLoggedIn()" to="/register">Register</router-link>
            </div>
        </div>
    </nav>
</template>

<script>
import { isLoggedIn } from "@/utils/auth";

export default {
    name: "navbar",
    methods: {
        isLoggedIn
    }
}
</script>
