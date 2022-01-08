import aprs_routes from "./routes/aprs";
import blog_routes from "./routes/blog";
import exams_routes from "./routes/exams";
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
      ...blog_routes,
      ...exams_routes,
      ...repeaters_routes,
    ],
  },
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
