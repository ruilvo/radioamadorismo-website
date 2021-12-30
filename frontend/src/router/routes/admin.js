import { RouterView } from "vue-router";

const routes_admin = [
  {
    name: "admin",
    path: "/admin/",
    meta: { requiresAuth: true },
    component: () => import("layouts/Cms.vue"),
    children: [
      {
        name: "admin-index",
        path: "",
        component: () => import("pages/cms/Index.vue"),
      },
      {
        name: "admin-blog",
        path: "blogue/",
        component: RouterView,
        children: [
          {
            name: "admin-blog-list",
            path: "",
            component: () => import("pages/cms/blog/PostList.vue"),
          },
          {
            name: "admin-blog-post-edit",
            path: "editar/:id/",
            component: () => import("pages/cms/blog/PostEdit.vue"),
            props: true,
          },
          {
            name: "cms-blog-post-new",
            path: "novo/",
            component: () => import("pages/cms/blog/PostCreate.vue"),
            props: true,
          },
        ],
      },
    ],
  },
];

export default routes_admin;
