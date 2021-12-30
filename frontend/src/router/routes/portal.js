const routes_portal = [
  {
    name: "portal",
    path: "/",
    component: () => import("layouts/Main.vue"),
    children: [
      {
        name: "portal-index",
        path: "",
        component: () => import("pages/portal/Index.vue"),
      },
      {
        name: "blog-detail",
        path: "blogue/:id",
        component: () => import("pages/portal/BlogPostDetail.vue"),
        props: true,
      },
    ],
  },
];

export default routes_portal;
