import { boot } from "quasar/wrappers";

import { api } from "boot/axios";

import useAuthStore from "src/stores/auth";

export default boot(({ router }) => {
  const authStore = useAuthStore();

  // https://www.smashingmagazine.com/2020/10/authentication-in-vue-js/

  router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
      if (!authStore.isAuthenticated) {
        next({ name: "login" });
        return;
      }
    }
    next();
  });

  router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.guest)) {
      if (authStore.isAuthenticated) {
        next({ name: "home" });
        return;
      }
    }
    next();
  });

  api.interceptors.response.use(undefined, function (error) {
    if (error) {
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        authStore.$reset();
        return router.push({ name: "login" });
      }
    }
    return Promise.reject(error);
  });
});
