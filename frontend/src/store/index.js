import { store } from "quasar/wrappers";
import { createPinia } from "pinia";

// I'm not sure Pinia plays well with quasar/wrappers/store...

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default store(function (/* { ssrContext } */) {
  const Store = createPinia();

  return Store;
});
