<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useStatsStore } from "@/stores/stats";

const stats = useStatsStore();
const online = ref(navigator.onLine);

async function update() {
  online.value = navigator.onLine;
  if (online.value) {
    await stats.flushQueue();
  }
}

onMounted(() => {
  window.addEventListener("online", update);
  window.addEventListener("offline", update);
  update();
});

onUnmounted(() => {
  window.removeEventListener("online", update);
  window.removeEventListener("offline", update);
});
</script>

<template>
  <transition name="fade">
    <div
      v-if="!online || stats.pending > 0"
      class="fixed top-0 left-0 right-0 z-40 py-1.5 px-4 text-center text-xs
             font-medium backdrop-blur-md"
      :class="online ? 'bg-accent/15 text-accent border-b border-accent/20'
                     : 'bg-red-500/15 text-red-300 border-b border-red-500/20'"
    >
      <template v-if="!online && stats.pending > 0">
        Оффлайн · {{ stats.pending }} в очереди
      </template>
      <template v-else-if="!online">
        Оффлайн · результаты сохранятся локально
      </template>
      <template v-else>
        Отправляем {{ stats.pending }} из очереди...
      </template>
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>