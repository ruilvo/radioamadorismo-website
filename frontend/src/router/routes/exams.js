import { RouterView } from "vue-router";

export const exams_routes = [
  {
    name: "exams-root",
    path: "exames/",
    component: RouterView,
    children: [
      {
        name: "exams",
        path: "",
        component: () => import("pages/exams/Exams.vue"),
      },
      {
        name: "exams-category-root",
        path: ":category/",
        component: RouterView,
        children: [
          {
            name: "exams-category",
            path: "",
            component: () => import("pages/exams/Exams.vue"),
            props: true,
          },
          {
            name: "exams-question",
            path: ":id/",
            component: () => import("pages/exams/Exams.vue"),
            props: true,
          },
        ],
      },
    ],
  },
];

export { exams_routes as default };
