const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/Index.vue") },
      {
        path: "login/",
        component: () => import("pages/auth/Login.vue"),
        meta: { guest: true },
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
      { path: "sobre/", component: () => import("pages/About.vue") },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
