import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "./style.css";
import { registerSW } from "virtual:pwa-register";
import { useThemeStore } from "./stores/theme";

registerSW({ immediate: true });

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);

useThemeStore().init();

app.mount("#app");