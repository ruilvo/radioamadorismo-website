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
    children: [
      {
        path: "",
        name: "Repeaters-Table",
        component: () =>
          import(
            /* webpackChunkName: "repeaters-table" */ "../components/repeaters/Table.vue"
          ),
      },
      {
        path: "mapa/",
        name: "Repeaters-Map",
        component: () =>
          import(
            /* webpackChunkName: "repeaters-map" */ "../components/repeaters/Map.vue"
          ),
      },
    ],
  },
  {
    path: "/swagger-ui",
    name: "Swagger",
    component: () =>
      import(/* webpackChunkName: "swagger" */ "../views/Swagger.vue"),
  },
];

const router = createRouter({
  mode: "history",
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
