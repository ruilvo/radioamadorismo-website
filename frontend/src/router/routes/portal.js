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
        name: "portal-repeaters",
        path: "repetidores/",
        component: () => import("pages/portal/Repeaters.vue"),
        children: [
          {
            name: "portal-repeaters-list",
            path: "",
            component: () => import("components/portal/repeaters/List.vue"),
          },
          {
            name: "portal-repeaters-map",
            path: "mapa/",
            component: () => import("components/portal/repeaters/Map.vue"),
          },
        ],
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
