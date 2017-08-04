<template>
    <section>
        <section class="hero is-light">
            <div class="hero-body">
                <div class="container">
                    <h1 class="title">
                        Login
                    </h1>
                </div>
            </div>
        </section>
        <section class="section container">
            <div class="columns is-centered">
                <div class="column is-half">
                    <nav class="panel">
                        <p class="panel-heading">Login</p>
                        <div class="panel-block">
                            <form>
                                <div class="field">
                                    <label class="label">Username</label>
                                    <div class="control has-icons-left">
                                        <input class="input" type="text" placeholder="Username">
                                        <span class="icon is-small is-left">
                                            <i class="fa fa-user"></i>
                                        </span>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </nav>
                </div>
            </div>
        </section>
    </section>
</template>

<script>
export default {
    name: "login"
}
</script>