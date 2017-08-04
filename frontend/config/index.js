var path = require("path");

module.exports = {
    build: {
        env: {},
        index: path.resolve(__dirname, "../dist/index.html"),
        assetsRoot: path.resolve(__dirname, "../dist"),
        assetsSubDirectory: "static",
        assetsPublicPath: "/",
        productionSourceMap: true
    },
    dev: {
        env: {},
        port: 8000,
        autoOpenBrowser: true,
        assetsSubDirectory: "static",
        assetsPublicPath: "/",
        proxyTable: {},
        cssSourceMap: false
    }
};