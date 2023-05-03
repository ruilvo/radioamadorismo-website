import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance } from 'axios';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
  }
}

axios.defaults.withCredentials = true;

const api = axios.create({ withCredentials: true });
api.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
api.defaults.xsrfCookieName = 'csrftoken';

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios;
  app.config.globalProperties.$api = api;
});

export { api };
