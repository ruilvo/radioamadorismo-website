const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/Index.vue") },
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
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
