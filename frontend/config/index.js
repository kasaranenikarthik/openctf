var path = require("path");

module.exports = {
    build: {
        env: {
            "API_URL": "/api"
        },
        index: path.resolve(__dirname, "../dist/index.html"),
        assetsRoot: path.resolve(__dirname, "../dist"),
        assetsSubDirectory: "static",
        assetsPublicPath: "/",
        productionSourceMap: true
    },
    dev: {
        env: {
            "API_URL": "http://localhost:7911"
        },
        port: 8000,
        autoOpenBrowser: true,
        assetsSubDirectory: "static",
        assetsPublicPath: "/",
        proxyTable: {},
        cssSourceMap: false
    }
};