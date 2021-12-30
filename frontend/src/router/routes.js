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
    children: [
      { path: "", component: () => import("pages/cms/Index.vue") },
      {
        path: "blogue/",
        component: () => import("pages/cms/blog/BlogPostList.vue"),
      },
      {
        name: "blog-post-edit",
        path: "blogue/editar/:id/",
        component: () => import("pages/cms/blog/BlogPostEdit.vue"),
        props: true,
      },
      {
        name: "blog-post-new",
        path: "blogue/novo/",
        component: () => import("pages/cms/blog/BlogPostCreate.vue"),
        props: true,
      },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
