import { RouterView } from "vue-router";

export const aprs_routes = [
  {
    name: "aprs",
    path: "aprs/",
    component: RouterView,
    children: [
      {
        name: "aprs-passcode",
        path: "passcode/",
        component: () => import("pages/aprs/AprsPasscode.vue"),
      },
    ],
  },
];

export { aprs_routes as default };
