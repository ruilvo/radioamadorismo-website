import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import titleMixin from "./mixins/titleMixin";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

createApp(App).mixin(titleMixin).use(router).mount("#app");
