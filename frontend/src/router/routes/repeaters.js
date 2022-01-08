import { RouterView } from "vue-router";

export const repeaters_routes = [
  {
    name: "repeaters",
    path: "repetidores/",
    component: RouterView,
    children: [
      {
        name: "repeaters-items",
        path: "",
        component: () => import("pages/Repeaters.vue"),
        children: [
          {
            name: "repeaters-list",
            path: "",
            component: () => import("components/RepeatersList.vue"),
          },
          {
            name: "repeaters-map",
            path: "mapa/",
            component: () => import("components/RepeatersMap.vue"),
          },
        ],
      },
      {
        name: "repeaters-item",
        path: ":id/",
        component: RouterView,
        children: [
          {
            name: "repeater-item-edit",
            path: "editar/",
            component: () => import("pages/RepeaterNotesEdit.vue"),
            props: true,
            meta: {
              requiresAuth: true,
            },
          },
        ],
      },
    ],
  },
];

export { repeaters_routes as default };
