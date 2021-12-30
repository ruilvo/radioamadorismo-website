import routes_portal from "./routes/portal";
import routes_auth from "./routes/auth";
import routes_admin from "./routes/admin";

const routes = [
  ...routes_portal,
  ...routes_auth,
  ...routes_admin,
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
