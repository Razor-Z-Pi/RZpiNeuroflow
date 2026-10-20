<script setup>
import { ref, onMounted } from "vue";
import { hasSeen, markSeen } from "@/utils/hints";
import AppIcon from "@/components/AppIcon.vue";

const props = defineProps({
  hintKey: { type: String, required: true },
  title: { type: String, default: "Совет" },
  text: { type: String, required: true },
});

const visible = ref(false);

onMounted(() => {
  visible.value = !hasSeen(props.hintKey);
});

function close() {
  visible.value = false;
  markSeen(props.hintKey);
}
</script>

<template>
  <transition name="hint">
    <div
      v-if="visible"
      class="mb-5 rounded-xl border border-violet/30 bg-violet/8
             p-3.5 flex items-start gap-3 relative"
    >
      <div
        class="w-8 h-8 shrink-0 rounded-lg bg-violet/20 border border-violet/30
               flex items-center justify-center text-violet"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 16v-4M12 8h.01" />
        </svg>
      </div>
      <div class="flex-1 min-w-0">
        <p class="font-semibold text-sm text-violet mb-0.5">{{ title }}</p>
        <p class="text-ink/80 text-xs leading-relaxed">{{ text }}</p>
      </div>
      <button
        class="shrink-0 w-6 h-6 rounded-md flex items-center justify-center
               text-muted hover:text-ink hover:bg-ink/5 transition"
        aria-label="Скрыть"
        @click="close"
      >
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M18 6L6 18M6 6l12 12" />
        </svg>
      </button>
    </div>
  </transition>
</template>

<style scoped>
.hint-enter-active,
.hint-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.hint-enter-from,
.hint-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>