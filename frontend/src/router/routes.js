const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/portal/Index.vue") },
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
    path: "/login/",
    component: () => import("layouts/EmptyLayout.vue"),
    children: [{ path: "", component: () => import("pages/auth/Login.vue") }],
    meta: { guest: true },
  },
  {
    path: "/cms/",
    component: () => import("layouts/CmsLayout.vue"),
    meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/portal/Index.vue") }],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
