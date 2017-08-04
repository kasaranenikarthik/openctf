var config = require("../config");
var path = require("path");
var rm = require("rimraf");
var webpack = require("webpack");
var webpackConfig = require("./webpack.prod.conf")

rm(path.join(config.build.assetsRoot, config.build.assetsSubDirectory), err => {
    if (err) throw err;
    webpack();
});
