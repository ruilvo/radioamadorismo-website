const brand = require("./brand.config.js");

module.exports = {
  prefix: "tw-",
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ...brand,
      },
    },
  },
  corePlugins: { preflight: false },
  plugins: [],
};
