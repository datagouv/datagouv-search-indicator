/* global module,process */
const path = require('path')
const webpack = require('webpack')
const VueLoaderPlugin = require('vue-loader/lib/plugin')

const PATH_PREFIX = process.env.PATH_PREFIX || '';

const css_loaders = [
  {loader: 'style-loader', options: {sourceMap: true}},
  {loader: 'css-loader', options: {sourceMap: true}},
  {loader: 'postcss-loader', options: {sourceMap: true}},
]

module.exports = function(env, argv) {
  const isProd = argv.mode === 'production'
  const config = {
    entry: [
      'core-js/stable',
      'regenerator-runtime/runtime',
      'whatwg-fetch',
      './src/main.js'
    ],
    output: {
      path: path.resolve(__dirname, './dist'),
      publicPath: `${PATH_PREFIX}/dist/`,
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
        {test: /\.vue$/, loader: 'vue-loader'},
        {test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader'},
        {test: /\.css$/, use: css_loaders},
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
      contentBase: path.resolve(__dirname),
      // noInfo: true,
      overlay: {
          warnings: true,
          errors: true
      },
      disableHostCheck: true,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
      },
      hot: true
    },
    performance: {
      hints: false
    },
    devtool: isProd ? 'source-map' : 'eval-source-map',
    plugins: [
      new webpack.DefinePlugin({
        PRODUCTION: JSON.stringify(isProd)
      }),
      new VueLoaderPlugin(),
    ]
  }

  return config
}
