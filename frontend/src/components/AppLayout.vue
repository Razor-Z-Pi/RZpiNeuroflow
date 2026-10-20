<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useThemeStore } from "@/stores/theme";
import AppIcon from "@/components/AppIcon.vue";

const auth = useAuthStore();
const theme = useThemeStore();
const router = useRouter();

const greeting = computed(() => {
  const h = new Date().getHours();
  if (h < 12) return "Доброе утро";
  if (h < 18) return "Добрый день";
  return "Добрый вечер";
});

function logout() {
  auth.logout();
  router.push("/login");
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-6 py-8">
    <header class="flex flex-wrap gap-4 items-center justify-between mb-10">
      <div class="flex items-center gap-3">
        <div
          class="w-10 h-10 rounded-xl bg-accent/15 border border-accent/30
                 flex items-center justify-center text-accent"
        >
          <AppIcon name="brain" :size="20" />
        </div>
        <div>
          <h1 class="text-lg font-bold leading-none text-text">
            {{ greeting }}, {{ auth.user?.username }}
          </h1>
          <p class="text-muted text-xs mt-1">Готов к тренировке?</p>
        </div>
      </div>

      <nav class="flex items-center gap-2">
        <router-link
          to="/"
          class="btn-ghost !py-2 !px-4 text-sm inline-flex items-center gap-2"
          exact-active-class="!border-accent/40 !text-accent"
        >
          <AppIcon name="reading" :size="16" />
          Тренировки
        </router-link>
        <router-link
          to="/stats"
          class="btn-ghost !py-2 !px-4 text-sm inline-flex items-center gap-2"
          active-class="!border-accent/40 !text-accent"
        >
          <AppIcon name="chart" :size="16" />
          Прогресс
        </router-link>
        <router-link
          to="/achievements"
          class="btn-ghost !py-2 !px-3 text-sm text-muted hover:text-ink"
          title="Достижения"
          active-class="!border-accent/40 !text-accent"
        >
          <AppIcon name="trophy" :size="16" />
        </router-link>
        <router-link
          to="/settings"
          class="btn-ghost !py-2 !px-3 text-sm text-muted hover:text-text"
          title="Настройки"
        >
          <AppIcon name="settings" :size="16" />
        </router-link>
        <button
          class="btn-ghost !py-2 !px-3 text-sm text-muted hover:text-text"
          :title="theme.theme === 'dark' ? 'Светлая тема' : 'Тёмная тема'"
          @click="theme.toggle()"
        >
          <AppIcon :name="theme.theme === 'dark' ? 'sun' : 'moon'" :size="16" />
        </button>
        <button
          class="btn-ghost !py-2 !px-3 text-sm text-muted hover:text-text"
          title="Выйти"
          @click="logout"
        >
          <AppIcon name="logout" :size="16" />
        </button>
      </nav>
    </header>

    <slot />
  </div>
</template>