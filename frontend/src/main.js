import Vue from "vue";
import App from "./App";
import router from "./router";

// not terribly important
Vue.config.productionTip = false;

new Vue({
    el: "#app",
    router: router,
    render: function (h) { return h(App); },
    template: "<App/>",
    components: { App }
});
