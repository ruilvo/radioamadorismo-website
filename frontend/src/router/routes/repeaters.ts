export const repeaters_routes = [
  {
    name: 'repeaters',
    path: 'repeaters/',
    component: () => import('pages/RepeatersPage.vue'),
    children: [
      {
        name: 'repeater_detail',
        path: ':id',
        component: () => import('pages/RepeaterDetailPage.vue'),
        props: true,
      },
    ],
  },
];

export { repeaters_routes as default };
