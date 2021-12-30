import { RouterView } from "vue-router";

const routes_cms = [
  {
    name: "cms",
    path: "/cms/",
    meta: { requiresAuth: true },
    component: () => import("layouts/Cms.vue"),
    children: [
      {
        name: "cms-index",
        path: "",
        component: () => import("pages/cms/Index.vue"),
      },
      {
        name: "cms-blog",
        path: "blogue/",
        component: RouterView,
        children: [
          {
            name: "cms-blog-list",
            path: "",
            component: () => import("pages/cms/blog/PostList.vue"),
          },
          {
            name: "cms-blog-post-edit",
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

export default routes_cms;
