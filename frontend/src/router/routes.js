import routes_portal from "./routes/portal";
import routes_auth from "./routes/auth";
import routes_cms from "./routes/cms";

const routes = [
  ...routes_portal,
  ...routes_auth,
  ...routes_cms,
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/Error404.vue"),
  },
];

export default routes;
