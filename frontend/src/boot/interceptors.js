import { boot } from "quasar/wrappers";

import { useRouter } from "vue-router";

import axios from "axios";

export default boot(() => {
  const router = useRouter();

  axios.interceptors.response.use(undefined, function (error) {
    if (error) {
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        return router.push("/login");
      }
    }
  });
});
