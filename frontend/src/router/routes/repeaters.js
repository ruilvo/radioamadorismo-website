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
        component: () => import("pages/repeaters/Repeaters.vue"),
        children: [
          {
            name: "repeaters-tree",
            path: "",
            component: () => import("components/repeaters/RepeatersTree.vue"),
          },
          {
            name: "repeaters-map",
            path: "mapa/",
            component: () => import("components/repeaters/RepeatersMap.vue"),
          },
        ],
      },
      {
        name: "repeaters-item",
        path: ":id/",
        component: RouterView,
        children: [
          {
            name: "repeater-notes-edit",
            path: "editar/",
            component: () => import("pages/repeaters/NotesEdit.vue"),
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
