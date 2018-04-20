const path = require("path");
const webpack = require("webpack");

const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  entry : {
    bundle : ["./src/main.js", ],
  },
  resolve : {
    extensions : [".js", ".html", ],
  },
  output : {
    path :     path.join(__dirname, "generated"),
    filename : "[name].[hash].js",
  },
  mode :   "development",
  module : {
    rules : [
      {
        test :    /\.html$/,
        exclude : /node_modules/,
        use :     {
          loader :  "svelte-loader",
          options : {
            cascade :   false,
            store :     true,
            hotReload : true,
          },
        },
      }, {
        test : /\.scss$/,
        use :  [
          {loader : "style-loader", options : {hmr : true, }, },
          {loader : "css-loader", },
          {loader : "sass-loader", },
        ],
      },
    ],
  },
  devtool :   "sourcemap",
  devServer : {
    contentBase : path.join(__dirname, "generated"),
    port :        2600,
  },
  plugins : [
    new MiniCssExtractPlugin({}),
    new HtmlWebpackPlugin({
      title :  "OpenCTF",
      inject : "body",
      meta :   {viewport : "width=device-width, initial-scale=1, shrink-to-fit=no", },
      minify : true,
      hash :   true,
      cache :  true,
    }),
    new webpack.DefinePlugin({
      API_BASE : JSON.stringify("http://localhost:2601/api"),
    }),
  ],
};
