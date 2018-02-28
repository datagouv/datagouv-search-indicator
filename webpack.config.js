/* global module,process */
const path = require('path')
const webpack = require('webpack')

const isProd = process.env.NODE_ENV === 'production'

const scss_loaders = [
   {loader: 'vue-style-loader', options: {sourceMap: true}},
   {loader: 'css-loader', options: {sourceMap: true}},
   {loader: 'postcss-loader', options: {sourceMap: true}},
   {loader: 'sass-loader', options: {sourceMap: true, outputStyle: 'compact'}},
]

const sass_loaders = [
   {loader: 'vue-style-loader', options: {sourceMap: true}},
   {loader: 'css-loader', options: {sourceMap: true}},
   {loader: 'postcss-loader', options: {sourceMap: true}},
   {loader: 'sass-loader', options: {sourceMap: true, indentedSyntax: true, outputStyle: 'compact'}},
]

const stylus_loaders = [
   {loader: 'vue-style-loader', options: {sourceMap: true}},
   {loader: 'css-loader', options: {sourceMap: true}},
   {loader: 'postcss-loader', options: {sourceMap: true}},
   {loader: 'stylus-loader', options: {sourceMap: true, outputStyle: 'compact'}},
]

const css_loaders = [
   {loader: 'style-loader', options: {sourceMap: true}},
   {loader: 'css-loader', options: {sourceMap: true}},
   {loader: 'postcss-loader', options: {sourceMap: true}},
]

module.exports = {
  entry: ['@babel/polyfill', 'whatwg-fetch', './src/main.js'],
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: './dist/',
    filename: 'build.js'
  },
  resolve: {
    extensions: ['.js', '.vue'],
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      'public': path.resolve(__dirname, './public')
    }
  },
  module: {
    rules: [
      {test: /\.vue$/, loader: 'vue-loader', options: {
          loaders: {
              css: css_loaders,
              scss: scss_loaders,
              sass: sass_loaders,
          }
      }},
      {test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader'},
      {test: /\.scss$/, use: scss_loaders},
      {test: /\.css$/, use: css_loaders},
      {test: /\.styl$/, use: stylus_loaders},
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          objectAssign: 'Object.assign'
        }
      },
    ]
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true
  },
  performance: {
    hints: false
  },
  devtool: isProd ? 'source-map' : 'eval-source-map',
  plugins: []
}

if (isProd) {
  module.exports.plugins.push(
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  )
}
