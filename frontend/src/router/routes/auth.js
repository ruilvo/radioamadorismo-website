const routes_auth = [
  {
    name: "auth",
    path: "/auth/",
    meta: { guest: true },
    component: () => import("layouts/Empty.vue"),
    children: [
      {
        name: "auth-login",
        path: "login/",
        component: () => import("pages/auth/Login.vue"),
      },
    ],
  },
];

export default routes_auth;
