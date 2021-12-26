import { boot } from "quasar/wrappers";

import axios from "axios";

import { useAuthStore } from "src/stores/auth";

export default boot(({ router }) => {
  const authStore = useAuthStore();

  // https://www.smashingmagazine.com/2020/10/authentication-in-vue-js/

  router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
      if (authStore.isAuthenticated) {
        next();
        return;
      }
      next("/login");
    } else {
      next();
    }
  });

  router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.guest)) {
      if (authStore.isAuthenticated) {
        next("/");
        return;
      }
      next();
    } else {
      next();
    }
  });

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
