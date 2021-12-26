import { boot } from "quasar/wrappers";

import axios from "axios";

const api = axios.create({ withCredentials: true });

api.defaults.xsrfHeaderName = "X-CSRFTOKEN";
api.defaults.xsrfCookieName = "csrftoken";

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios;
  app.config.globalProperties.$api = api;
});

export { api };
