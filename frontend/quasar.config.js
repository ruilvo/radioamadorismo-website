/* eslint-env node */

/*
 * This file runs in a Node context (it's NOT transpiled by Babel), so use only
 * the ES6 features that are supported by your Node version. https://node.green/
 */

/* eslint-disable @typescript-eslint/no-var-requires */

const { configure } = require('quasar/wrappers');

// Full list of options:
// https://v2.quasar.dev/quasar-cli-webpack
module.exports = configure(function () {
  return {
    supportTS: {
      tsCheckerConfig: {
        eslint: {
          enabled: true,
          files: './src/**/*.{ts,tsx,js,jsx,vue}',
        },
      },
    },

    preFetch: true,

    boot: ['axios'],

    css: ['app.scss'],

    extras: ['roboto-font', 'material-icons'],

    build: {
      vueRouterMode: 'history',

      // This fixes hot-reload issues when using Docker + WSL2
      extendWebpack(cfg) {
        cfg.watchOptions = {
          aggregateTimeout: 200,
          poll: 1000,
        };
      },
    },

    devServer: {
      server: {
        type: 'http',
      },
      port: 8080,
      open: false,
    },

    framework: {
      lang: 'pt',
      plugins: ['LoadingBar'],
    },
  };
});
