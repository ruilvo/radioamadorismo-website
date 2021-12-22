const brand = require("./brand.config.js");

module.exports = {
  prefix: "tw-",
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    screens: {
      // $breakpoint-xs: 599px !default
      xs: "599px",
      // $breakpoint-sm: 1023px !default
      sm: "1023px",
      // $breakpoint-md: 1439px !default
      md: "1439px",
      // $breakpoint-lg: 1919px !default
      lg: "1919px",
    },
    extend: {
      colors: {
        ...brand,
      },
    },
  },
  corePlugins: { preflight: false },
  plugins: [],
};
