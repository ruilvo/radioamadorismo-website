import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import titleMixin from "./mixins/titleMixin";
import axios from "axios";
import "./assets/tailwind.css";

axios.defaults.withCredentials = true;

createApp(App).mixin(titleMixin).use(store).use(router).mount("#app");
