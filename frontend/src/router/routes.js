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
        name: "login",
        path: "login/",
        component: () => import("pages/Login.vue"),
      },
      {
        name: "blog-detail",
        path: "blogue/:id/",
        component: () => import("pages/BlogPostDetail.vue"),
        props: true,
      },
      {
        name: "blog-edit",
        path: "blogue/edit/:id/",
        component: () => import("pages/BlogPostCreateEdit.vue"),
        props: true,
      },
      {
        name: "blog-new",
        path: "blogue/novo/",
        component: () => import("pages/BlogPostCreateEdit.vue"),
      },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
