import { RouterView } from "vue-router";

export const blog_routes = [
  {
    name: "blog",
    path: "blogue/",
    component: RouterView,
    children: [
      {
        name: "blog-posts",
        path: "",
        component: () => import("pages/blog/Blog.vue"),
      },
      {
        name: "blog-posts-page",
        path: ":page/",
        component: () => import("pages/blog/Blog.vue"),
        props: true,
      },
      {
        name: "blog-post",
        path: "posts/",
        component: RouterView,
        children: [
          {
            name: "blog-post-create",
            path: "novo/",
            component: () => import("pages/blog/CreateEdit.vue"),
          },
          {
            name: "blog-post-item",
            path: ":id/",
            component: RouterView,
            children: [
              {
                name: "blog-post-detail",
                path: "",
                component: () => import("pages/blog/Post.vue"),
                props: true,
              },
              {
                name: "blog-post-edit",
                path: "editar/",
                component: () => import("pages/blog/CreateEdit.vue"),
                props: true,
              },
            ],
          },
        ],
      },
    ],
  },
];

export { blog_routes as default };
