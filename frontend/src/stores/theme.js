import { defineStore } from "pinia";

function applyTheme(theme) {
  const html = document.documentElement;
  html.classList.remove("light", "dark");
  html.classList.add(theme);
}

export const useThemeStore = defineStore("theme", {
  state: () => ({
    theme: localStorage.getItem("nf_theme") || "dark",
  }),
  actions: {
    init() {
      applyTheme(this.theme);
    },
    toggle() {
      this.theme = this.theme === "dark" ? "light" : "dark";
      localStorage.setItem("nf_theme", this.theme);
      applyTheme(this.theme);
    },
    set(theme) {
      this.theme = theme;
      localStorage.setItem("nf_theme", theme);
      applyTheme(theme);
    },
  },
});