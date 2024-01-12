var path = require('path');
var webpack = require('webpack');
require('es6-promise').polyfill()

var HtmlWebpackPlugin = require('html-webpack-plugin');

var HTMLWebpackPluginConfig = new HtmlWebpackPlugin({
  template: __dirname + '/public/index.html',
  hash: true,
  filename: 'index.html',
  inject: 'body'
});

var HotReloader = new webpack.HotModuleReplacementPlugin();

module.exports = {
  devtool: 'source-map',
  entry: [
    'webpack-dev-server/client?http://0.0.0.0:8080',
    'webpack/hot/dev-server',
    './src/index.jsx'
  ],
  output: {
    path: __dirname + '/dist',
    filename: 'bundle.js',
    publicPath: '/'
  },
  resolve: {
    extensions: ['', '.js', '.jsx']
  },
  module: {
    noParse: [/jszip.js$/],
    loaders: [
      {
        test: /.jsx?$/,
        loader: 'react-hot!babel',
        include: path.join(__dirname, 'src')
      },
      {
        exclude: /node_modules/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react', 'stage-0', 'stage-1'],
          plugins: ["transform-decorators-legacy"]
        },
      }
    ]
  },
  externals: {
    'Config': JSON.stringify({
      apiUrl: "http://0.0.0.0:5000/api",
      columnParameterName: 'columns',
      discussionLinkColumnName: 'discussion'
    })
  },
  plugins: [HTMLWebpackPluginConfig, HotReloader],
  devServer: {
    contentBase: __dirname + '/dist',
    hot: true,
    historyApiFallback: true
  }
};