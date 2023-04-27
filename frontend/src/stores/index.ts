import { store } from 'quasar/wrappers';
import { createPinia } from 'pinia';
import { Router } from 'vue-router';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

declare module 'pinia' {
  export interface PiniaCustomProperties {
    readonly router: Router;
  }
}
export default store((/* { ssrContext } */) => {
  const pinia = createPinia();

  pinia.use(piniaPluginPersistedstate);

  return pinia;
});
