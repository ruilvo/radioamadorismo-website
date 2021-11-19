import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import titleMixin from "./mixins/titleMixin";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "leaflet/dist/leaflet.css";

createApp(App).mixin(titleMixin).use(router).mount("#app");
