import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { VitePWA } from "vite-plugin-pwa";
import path from "node:path";

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["icons/*.png"],
      manifest: {
        name: "NeuroFlow — тренировка мозга",
        short_name: "NeuroFlow",
        description:
          "Скорочтение, память, внимание и мышление по методикам Джима Квика и Томаса Франка.",
        theme_color: "#0B0F1A",
        background_color: "#0B0F1A",
        display: "standalone",
        start_url: "/",
        scope: "/",
        orientation: "portrait",
        lang: "ru",
        icons: [
          {
            src: "/icons/icon-192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "/icons/icon-512.png",
            sizes: "512x512",
            type: "image/png",
          },
          {
            src: "/icons/icon-512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable",
          },
        ],
      },
      workbox: {
        globPatterns: ["**/*.{js,css,html,svg,png,ico,woff2}"],
        navigateFallback: "/index.html",
        navigateFallbackDenylist: [/^\/api/],
        runtimeCaching: [
          {
            // API-статистика: сначала сеть, потом кэш
            urlPattern: ({ url }) => url.pathname.startsWith("/api/stats"),
            handler: "NetworkFirst",
            options: {
              cacheName: "api-stats",
              networkTimeoutSeconds: 5,
              expiration: { maxEntries: 50, maxAgeSeconds: 60 * 60 * 24 },
            },
          },
          {
            // Профиль: тоже NetworkFirst
            urlPattern: ({ url }) => url.pathname.startsWith("/api/users"),
            handler: "NetworkFirst",
            options: {
              cacheName: "api-users",
              networkTimeoutSeconds: 5,
              expiration: { maxEntries: 10, maxAgeSeconds: 60 * 60 * 24 },
            },
          },
          {
            // Шрифты Google
            urlPattern: /^https:\/\/fonts\.(googleapis|gstatic)\.com\/.*/i,
            handler: "CacheFirst",
            options: {
              cacheName: "google-fonts",
              expiration: { maxEntries: 20, maxAgeSeconds: 60 * 60 * 24 * 365 },
            },
          },
        ],
      },
      devOptions: {
        enabled: false, // включай true только если хочешь тестировать SW в dev
      },
    }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
  },
});