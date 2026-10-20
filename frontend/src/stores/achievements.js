import { defineStore } from "pinia";
import api from "@/api/client";

export const useAchievementsStore = defineStore("achievements", {
  state: () => ({
    items: [],
    loading: false,
  }),
  getters: {
    unlocked: (s) => s.items.filter((a) => a.unlocked),
    locked: (s) => s.items.filter((a) => !a.unlocked),
    total: (s) => s.items.length,
    unlockedCount: (s) => s.items.filter((a) => a.unlocked).length,
  },
  actions: {
    async fetch() {
      this.loading = true;
      try {
        const { data } = await api.get("/api/stats/achievements");
        this.items = data;
      } finally {
        this.loading = false;
      }
    },
  },
});