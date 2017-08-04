var config = require("../config");
var express = require("express");
var opn = require("opn");
var path = require("path");
var proxyMiddleware = require("http-proxy-middleware");
var webpack = require("webpack");
var webpackConfig = require("./webpack.dev.conf");

var app = express();
var compiler = webpack(webpackConfig);
var port = process.env.PORT || config.dev.port;
var proxyTable = config.dev.proxyTable;

var devMiddleware = require("webpack-dev-middleware")(compiler, {
    publicPath: webpackConfig.output.publicPath,
    quiet: true
});

var hotMiddleware = require("webpack-hot-middleware")(compiler, {
    log: false,
    heartbeat: 2000
});

compiler.plugin("compilation", function (compilation) {
    compilation.plugin("html-webpack-plugin-after-emit", function (data, callback) {
        hotMiddleware.publish({ action: "reload" });
        callback();
    });
});

Object.keys(proxyTable).forEach(function (context) {
    var options = proxyTable[context];
    if (typeof options === "string") {
        options = { target: options };
    }
    app.use(proxyMiddleware(options.filter || context, options));
});

app.use(require("connect-history-api-fallback"));
app.use(devMiddleware);
app.use(hotMiddleware);

var staticPath = path.posix.join(config.dev.assetsPublicPath, config.dev.assetsSubDirectory);
app.use(staticPath, express.static("./static"));

var uri = "http://localhost:" + port;

var _resolve;
var readyPromise = new Promise(resolve => {
    _resolve = resolve;
});

console.log("[.] Starting dev server...");
devMiddleware.waitUntilValid(() => {
    console.log("[+] Listening at " + uri + "\n");
    if (!!config.dev.autoOpenBrowser && process.env.NODE_ENV !== "testing") {
        // don't do this for now lol
        // opn(uri);
    }
    _resolve();
});

var server = app.listen(port);

module.exports = {
    ready: readyPromise,
    close: () => {
        server.close();
    }
};