var baseWebpackConfig = require("./webpack.base.conf");
var config = require("../config");
var FriendlyErrorsPlugin = require("friendly-errors-webpack-plugin");
var HtmlWebpackPlugin = require("html-webpack-plugin");
var merge = require("webpack-merge");
var utils = require("./utils");
var webpack = require("webpack");

Object.keys(baseWebpackConfig.entry).forEach(function (name) {
    baseWebpackConfig.entry[name] = ["./build/dev-client"].concat(baseWebpackConfig.entry[name])
});

module.exports = merge(baseWebpackConfig, {
    module: {
        rules: utils.styleLoaders({ sourceMap: config.dev.cssSourceMap })
    },
    devtool: "#cheap-module-eval-source-map",
    plugins: [
        new webpack.DefinePlugin({
            "process.env": config.dev.env
        }),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(),
        new HtmlWebpackPlugin({
            filename: "index.html",
            template: "index.html",
            inject: true
        }),
        new FriendlyErrorsPlugin()
    ]
});