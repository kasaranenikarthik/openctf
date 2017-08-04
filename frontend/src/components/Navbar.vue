<template>
    <nav class="navbar container">
        <div class="navbar-brand">
            <a class="navbar-item" href="/">
                OpenCTF
            </a>
            <div class="navbar-burger" data-target="mainNavbar">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        <div id="mainNavbar" class="navbar-menu">
            <div class="navbar-start">
                <div class="navbar-item has-dropdown is-hoverable">
                    <div class="navbar-link is-active">About</div>
                    <div class="navbar-dropdown ">
                        <a class="navbar-item" href="/documentation/overview/start/">Overview</a>
                        <a class="navbar-item" href="http://bulma.io/documentation/modifiers/syntax/">Modifiers</a>
                        <a class="navbar-item" href="http://bulma.io/documentation/grid/columns/">Grid</a>
                        <a class="navbar-item" href="http://bulma.io/documentation/layout/container/">Layout</a>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: "navbar"
}
</script>
