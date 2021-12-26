import { route } from "quasar/wrappers";

import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";

import { useAuthStore } from "src/stores/auth";

import routes from "./routes";

export default route(function () {
  const authStore = useAuthStore();

  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === "history"
    ? createWebHistory
    : createWebHashHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(
      process.env.MODE === "ssr" ? void 0 : process.env.VUE_ROUTER_BASE
    ),
  });

  Router.beforeEach((to, from, next) => {
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

  Router.beforeEach((to, from, next) => {
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

  return Router;
});
