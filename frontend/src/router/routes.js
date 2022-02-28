import aprs_routes from "./routes/aprs";
import repeaters_routes from "./routes/repeaters";

const routes = [
  {
    name: "index",
    path: "/",
    component: () => import("layouts/Main.vue"),
    children: [
      // Main page
      {
        name: "home",
        path: "",
        component: () => import("pages/Index.vue"),
      },
      // Auth
      {
        name: "login",
        path: "login/",
        component: () => import("pages/Login.vue"),
        meta: {
          guest: true,
        },
      },
      ...aprs_routes,
      ...repeaters_routes,
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
