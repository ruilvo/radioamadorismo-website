import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/repetidores",
    name: "Repeaters",
    component: () =>
      import(/* webpackChunkName: "repeaters" */ "../views/Repeaters.vue"),
  },
  {
    path: "/swagger-ui",
    name: "Swagger",
    component: () =>
      import(/* webpackChunkName: "swagger" */ "../views/Swagger.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
