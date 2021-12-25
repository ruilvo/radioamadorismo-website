const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/Index.vue") },
      {
        path: "login/",
        // TODO: transform this into an actually decent page
        component: () => import("components/auth/LoginForm.vue"),
      },
      {
        path: "repetidores/",
        component: () => import("pages/Repeaters.vue"),
        children: [
          {
            path: "",
            component: () => import("components/repeaters/RepeatersList.vue"),
          },
          {
            path: "mapa/",
            component: () => import("components/repeaters/RepeatersMap.vue"),
          },
        ],
      },
      { path: "swagger/", component: () => import("pages/Swagger.vue") },
      { path: "sobre/", component: () => import("pages/About.vue") },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
