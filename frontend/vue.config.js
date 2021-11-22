module.exports = {
  devServer: {
    proxy: {
      "^/api": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
      "^/static": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
    },
  },
};
