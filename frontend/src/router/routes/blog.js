import { RouterView } from "vue-router";

export const blog_routes = [
  {
    name: "blog",
    path: "blogue/",
    component: RouterView,
    children: [
      {
        name: "blog-post",
        path: ":id/",
        component: RouterView,
        children: [
          {
            name: "blog-post-detail",
            path: "",
            component: () => import("pages/BlogPostDetail.vue"),
            props: true,
          },
          {
            name: "blog-post-edit",
            path: "editar/",
            component: () => import("pages/BlogPostCreateEdit.vue"),
            props: true,
            meta: {
              requiresAuth: true,
            },
          },
        ],
      },
      {
        name: "blog-post-new",
        path: "novo/",
        component: () => import("pages/BlogPostCreateEdit.vue"),
        meta: {
          requiresAuth: true,
        },
      },
    ],
  },
];

export { blog_routes as default };
