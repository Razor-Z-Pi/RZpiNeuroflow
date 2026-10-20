<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import AppIcon from "@/components/AppIcon.vue";

const queue = ref([]);
const current = ref(null);
const visible = ref(false);

let hideTimeout = null;
let gapTimeout = null;

function push(achievement) {
  if (!achievement || !achievement.code) return;
  queue.value.push(achievement);
  if (!current.value) {
    next();
  }
}

function next() {
  if (!queue.value.length) {
    current.value = null;
    visible.value = false;
    return;
  }
  current.value = queue.value.shift();
  visible.value = true;

  // Держим плашку 3.5 секунды, потом прячем и через 300 мс показываем следующую
  hideTimeout = setTimeout(() => {
    visible.value = false;
    gapTimeout = setTimeout(next, 300);
  }, 3500);
}

function close() {
  clearTimeout(hideTimeout);
  clearTimeout(gapTimeout);
  visible.value = false;
  setTimeout(() => {
    current.value = null;
    next();
  }, 250);
}

onMounted(() => {
  window.__nf_achievement_push = push;
});

onUnmounted(() => {
  clearTimeout(hideTimeout);
  clearTimeout(gapTimeout);
  if (window.__nf_achievement_push === push) {
    delete window.__nf_achievement_push;
  }
});
</script>

<template>
  <transition name="toast">
    <div
      v-if="visible && current"
      class="fixed top-4 left-1/2 -translate-x-1/2 z-50
             card !p-4 border-accent/40 shadow-2xl
             flex items-center gap-3 min-w-[320px] max-w-md
             bg-panel"
      role="status"
      aria-live="polite"
    >
      <div
        class="w-12 h-12 shrink-0 rounded-xl bg-accent/15 border border-accent/30
               flex items-center justify-center text-accent"
      >
        <AppIcon :name="current.icon || 'check'" :size="22" />
      </div>

      <div class="flex-1 min-w-0">
        <p class="text-[10px] uppercase tracking-wider text-muted font-semibold mb-0.5">
          Достижение
        </p>
        <p class="font-bold leading-tight text-text">
          {{ current.title }}
        </p>
        <p class="text-muted text-xs mt-0.5 truncate">
          {{ current.description }}
        </p>
      </div>

      <button
        class="shrink-0 w-7 h-7 rounded-lg flex items-center justify-center
               text-muted hover:text-text hover:bg-text/5 transition"
        aria-label="Закрыть"
        @click="close"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M18 6L6 18M6 6l12 12" />
        </svg>
      </button>

      <!-- Прогресс-полоска: визуально показывает, сколько плашка ещё провисит -->
      <div class="absolute bottom-0 left-0 right-0 h-0.5 bg-text/5 overflow-hidden rounded-b-2xl">
        <div class="h-full bg-accent animate-toast-progress" />
      </div>
    </div>
  </transition>
</template>

<style scoped>
.toast-enter-active {
  transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toast-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translate(-50%, -20px);
}
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -10px);
}
</style>