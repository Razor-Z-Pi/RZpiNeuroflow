import { defineStore } from "pinia";
import api from "@/api/client";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("nf_token") || null,
    user: null,
  }),
  getters: {
    isAuthenticated: (s) => !!s.token,
  },
  actions: {
    setToken(token) {
      this.token = token;
      localStorage.setItem("nf_token", token);
    },
    async register(email, username, password) {
      const { data } = await api.post("/api/auth/register", {
        email,
        username,
        password,
      });
      this.setToken(data.access_token);
      await this.fetchMe();
    },
    async login(email, password) {
      const { data } = await api.post("/api/auth/login", { email, password });
      this.setToken(data.access_token);
      await this.fetchMe();
    },
    async fetchMe() {
      const { data } = await api.get("/api/users/me");
      this.user = data;
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("nf_token");
    },
    async saveBaseline(payload) {
        const { data } = await api.post("/api/users/baseline", payload);
        this.user = data;
    },
    async changePassword(currentPassword, newPassword) {
      await api.post("/api/users/password", {
        current_password: currentPassword,
        new_password: newPassword,
      });
    },
    async deleteAccount() {
      await api.delete("/api/users/me");
      this.logout();
    },
  },
});