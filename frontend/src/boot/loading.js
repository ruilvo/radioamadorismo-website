import { boot } from "quasar/wrappers";

import { LoadingBar } from "quasar";

export default boot(({ router }) => {
  router.beforeResolve((to, from, next) => {
    if (to.name) {
      LoadingBar.start();
    }
    next();
  });

  router.afterEach(() => {
    LoadingBar.stop();
  });
});
