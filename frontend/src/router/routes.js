const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/portal/Index.vue") },
      {
        path: "login/",
        component: () => import("pages/auth/Login.vue"),
        meta: { guest: true },
      },
      {
        path: "repetidores/",
        component: () => import("pages/portal/Repeaters.vue"),
        children: [
          {
            path: "",
            component: () =>
              import("components/portal/repeaters/RepeatersList.vue"),
          },
          {
            path: "mapa/",
            component: () =>
              import("components/portal/repeaters/RepeatersMap.vue"),
          },
        ],
      },
      { path: "sobre/", component: () => import("pages/portal/About.vue") },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
