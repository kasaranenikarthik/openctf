<template>
    <div id="app">
        <navbar></navbar>
        <img src="./assets/logo.png" />
        <router-view></router-view>
    </div>
</template>

<script>
import Home from "./components/Home";
import Navbar from "./components/Navbar";

export default {
    name: "app",
    components: {
        Navbar,
        Home
    }
}
</script>
