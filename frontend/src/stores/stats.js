import { defineStore } from "pinia";
import api from "@/api/client";
import { enqueue, getQueue, clearQueue } from "@/utils/offlineQueue";

export const useStatsStore = defineStore("stats", {
  state: () => ({
    stats: null,
    loading: false,
    pending: getQueue().length,
  }),
  actions: {
    async fetch() {
      this.loading = true;
      try {
        const { data } = await api.get("/api/stats/me");
        this.stats = data;
      } finally {
        this.loading = false;
      }
    },

    async submitExercise(payload) {
      if (navigator.onLine) {
        try {
          const { data } = await api.post("/api/exercises/submit", payload);

          // Показать достижения, если разблокировались
          if (data?.unlocked_achievements?.length) {
            for (const ach of data.unlocked_achievements) {
              window.__nf_achievement_push?.(ach);
            }
          }

          await this.flushQueue();
          await this.fetch();
          return data;
        } catch (e) {
          if (!e.response) {
            enqueue(payload);
            this.pending = getQueue().length;
            return { offline: true };
          }
          throw e;
        }
      }

      enqueue(payload);
      this.pending = getQueue().length;
      return { offline: true };
    },

    async flushQueue() {
      if (!navigator.onLine) return;
      const queue = getQueue();
      if (!queue.length) return;

      clearQueue();
      for (const item of queue) {
        const { _queuedAt, ...payload } = item;
        try {
          await api.post("/api/exercises/submit", payload);
        } catch {
          // Если одна запись не прошла — вернём её в очередь
          enqueue(payload);
        }
      }
      this.pending = getQueue().length;
      await this.fetch();
    },

    async exportCsv() {
      const response = await api.get("/api/stats/export/csv", {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      const disposition = response.headers?.["content-disposition"] || "";
      const match = disposition.match(/filename="?([^"]+)"?/);
      link.setAttribute("download", match ? match[1] : "neuroflow.csv");
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    },
  },
});