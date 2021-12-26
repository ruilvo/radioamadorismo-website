/*
 * This file runs in a Node context (it's NOT transpiled by Babel), so use only
 * the ES6 features that are supported by your Node version. https://node.green/
 */

// Configuration for your app
// https://quasar.dev/quasar-cli/quasar-conf-js

/* eslint-disable @typescript-eslint/no-var-requires */

/* eslint-env node */
const ESLintPlugin = require("eslint-webpack-plugin");
const { configure } = require("quasar/wrappers");
const brand = require("./brand.config.js");

module.exports = configure(function () {
  return {
    // https://quasar.dev/quasar-cli/supporting-ts
    supportTS: true,

    // app boot file (/src/boot)
    // --> boot files are part of "main.js"
    // https://quasar.dev/quasar-cli/boot-files
    boot: ["axios", "pinia", "auth"],

    // https://quasar.dev/quasar-cli/quasar-conf-js#Property%3A-css
    css: ["app.scss", "tw.css"],

    // https://github.com/quasarframework/quasar/tree/dev/extras
    extras: [
      "roboto-font", // optional, you are not bound to it
      "material-icons", // optional, you are not bound to it
    ],

    // Full list of options: https://quasar.dev/quasar-cli/quasar-conf-js#Property%3A-build
    build: {
      vueRouterMode: "history", // available values: 'hash', 'history'

      // this is a configuration passed on
      // to the underlying Webpack
      devtool: "source-map",

      // https://quasar.dev/quasar-cli/handling-webpack
      // "chain" is a webpack-chain object https://github.com/neutrinojs/webpack-chain
      chainWebpack(chain) {
        chain
          .plugin("eslint-webpack-plugin")
          .use(ESLintPlugin, [{ extensions: ["js", "vue"] }]);
      },

      // This fixed hot-reload issues when using Docker + WSL2
      extendWebpack(cfg) {
        cfg.watchOptions = {
          aggregateTimeout: 200,
          poll: 1000,
        };
      },
    },

    // Full list of options: https://quasar.dev/quasar-cli/quasar-conf-js#Property%3A-devServer
    devServer: {
      server: {
        type: "http",
      },
      port: 8080,
      open: true, // opens browser window automatically
      proxy: {
        "/admin": {
          target: "http://backend:8000",
        },
        "/cms": {
          target: "http://backend:8000",
        },
        "/api": {
          target: "http://backend:8000",
        },
        "/static": {
          target: "http://backend:8000",
        },
        "/media": {
          target: "http://backend:8000",
        },
      },
    },

    // https://quasar.dev/quasar-cli/quasar-conf-js#Property%3A-framework
    framework: {
      config: { brand: brand },

      // iconSet: 'material-icons', // Quasar icon set
      lang: "pt", // Quasar language pack

      // Quasar plugins
      plugins: [],
    },

    // animations: 'all', // --- includes all animations
    // https://quasar.dev/options/animations
    animations: [],
  };
});
