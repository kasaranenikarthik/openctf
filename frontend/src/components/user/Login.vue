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
        <div class="hero-body">
            <div class="container">
                <div class="columns is-centered">
                    <div class="column is-6">
                        <div class="login-form">
                            <div class="field">
                                <div class="control has-icons-left has-icons-right">
                                    <input class="input is-large" type="text" placeholder="email or username" autocomplete="off" autofocus>
                                    <span class="icon is-left">
                                        <i class="fa fa-user"></i>
                                    </span>
                                </div>
                            </div>
                            <div class="field">
                                <div class="control has-icons-left has-icons-right">
                                    <input class="input is-large" type="password" placeholder="password">
                                    <span class="icon is-left">
                                        <i class="fa fa-asterisk"></i>
                                    </span>
                                </div>
                            </div>
                            <button class="button is-primary is-large is-fullwidth">Login</button>
                        </div>
                        <div class="section forgot-password">
                            <p class="has-text-centered">
                                <a href="javascript:void(0);">Forgot password</a>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: "login"
}
</script>

<style lang="scss" scoped>
.avatar img {
    border-radius: 100%;
}
</style>