import { boot } from "quasar/wrappers";

import { useRouter } from "vue-router";

import axios from "axios";

import { useAuthStore } from "src/stores/auth";

export default boot(() => {
  const router = useRouter();
  const authStore = useAuthStore();

  // https://www.smashingmagazine.com/2020/10/authentication-in-vue-js/
  // 4.Handling Expired Token (Forbidden Requests)

  axios.interceptors.response.use(undefined, function (error) {
    if (error) {
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        authStore.logout();
        return router.push("/login");
      }
    }
  });
});
