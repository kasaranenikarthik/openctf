// const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin")

const mode = process.env.NODE_ENV || "development";
const prod = mode === "production";

module.exports = {
  entry : {
    bundle : ["./src/main.js", ],
  },
  resolve : {
    extensions : [".js", ".html", ],
  },
  output : {
    path :          __dirname + "/public",
    filename :      "[name].js",
    chunkFilename : "[name].[id].js",
  },
  module : {
    rules : [
      {
        test :    /\.html$/,
        exclude : /node_modules/,
        use :     {
          loader :  "svelte-loader",
          options : {
            emitCss :   true,
            cascade :   false,
            store :     true,
            hotReload : true,
          },
        },
      },
      {
        test : /\.scss$/,
        use :  [ "style-loader", "css-loader", "sass-loader" ],
      },
    ],
  },
  mode,
  plugins : [
    new HtmlWebpackPlugin({
      title :  "OpenCTF",
      inject : "head",
      meta :   {viewport : "width=device-width, initial-scale=1, shrink-to-fit=no", },
      minify : true,
      hash :   true,
      cache :  true,
    }),
  ],
  devtool : prod ? false : "source-map",
};
