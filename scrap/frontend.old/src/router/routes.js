const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/Index.vue") }],
  },

  // Portal routes
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

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
