export const repeaters_routes = [
  {
    name: 'repeaters-parent',
    path: 'repeaters/',
    children: [
      {
        name: 'repeaters',
        path: '',
        component: () => import('pages/RepeatersPage.vue'),
      },
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
