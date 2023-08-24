import { RouteRecordRaw } from 'vue-router';

import aprs_routes from './routes/aprs';
import repeaters_routes from './routes/repeaters';
import associations_routes from './routes/associations';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        name: 'home',
        path: '',
        component: () => import('pages/IndexPage.vue'),
      },
      ...aprs_routes,
      ...repeaters_routes,
      ...associations_routes,
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
