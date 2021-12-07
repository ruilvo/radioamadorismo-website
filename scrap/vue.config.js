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
      "^/openapi": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
      "^/admin": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
      "^/media": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
    },
  },
};
