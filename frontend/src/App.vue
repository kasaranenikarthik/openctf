<template>
    <div id="app">
        <!-- nav bar -->
        <navbar></navbar>
    
        <!-- main content -->
        <router-view id="main-view"></router-view>
    
        <!-- footer -->
        <footer class="footer">
            <div class="container">
                <div class="content has-text-centered">
                    <p>
                        Powered by
                        <b>
                            <a href="https://github.com/easyctf/openctf" target="_blank" rel="noopener">OpenCTF</a>
                        </b>, an open-source CTF platform.
                    </p>
                </div>
            </div>
        </footer>
    </div>
</template>

<script>
import Navbar from "./components/Navbar";

export default {
    name: "app",
    components: {
        Navbar
    }
}
</script>

<style lang="scss" scoped>
#main-view {
    min-height: 80vh;
}
</style>
