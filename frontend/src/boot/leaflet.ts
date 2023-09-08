import { boot } from 'quasar/wrappers';

import L from 'leaflet';

export default boot(() => {
  globalThis.L = L;
});
