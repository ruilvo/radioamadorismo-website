const routes = [
  {
    path: "/",
    component: () => import("layouts/Main.vue"),
    children: [
      {
        name: "index",
        path: "",
        component: () => import("pages/Index.vue"),
      },
      {
        name: "blog-detail",
        path: "blogue/:id",
        component: () => import("pages/BlogPostDetail.vue"),
        props: true,
      },
    ],
  },
  {
    path: "/login/",
    meta: { guest: true },
    component: () => import("layouts/Empty.vue"),
    children: [
      {
        name: "login",
        path: "",
        component: () => import("pages/Login.vue"),
      },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
