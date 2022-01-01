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
        name: "aprs-passcode",
        path: "aprs/passcode/",
        component: () => import("pages/AprsPasscode.vue"),
      },
      {
        name: "repeaters",
        path: "repetidores/",
        component: () => import("pages/Repeaters.vue"),
        children: [
          {
            name: "repeaters-list",
            path: "",
            component: () => import("components/RepeatersList.vue"),
          },
        ],
      },
      {
        name: "login",
        path: "login/",
        component: () => import("pages/Login.vue"),
        meta: {
          guest: true,
        },
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
        meta: {
          requiresAuth: true,
        },
      },
      {
        name: "blog-new",
        path: "blogue/novo/",
        component: () => import("pages/BlogPostCreateEdit.vue"),
        meta: {
          requiresAuth: true,
        },
      },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
