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
        name: "about",
        path: "sobre/",
        component: () => import("pages/portal/About.vue"),
      },
    ],
  },
];

export default routes_portal;
