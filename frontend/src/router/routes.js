import routes_portal from "./routes/portal";
import routes_auth from "./routes/auth";

const routes = [
  ...routes_portal,
  ...routes_auth,
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
