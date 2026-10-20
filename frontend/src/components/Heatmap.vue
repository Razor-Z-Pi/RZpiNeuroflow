<script setup>
import { computed, ref } from "vue";
import { buildHeatmap, levelFor } from "@/utils/heatmap";

const props = defineProps({
  history: { type: Array, default: () => [] },
  weeks: { type: Number, default: 26 },
});

const hovered = ref(null);

const cells = computed(() => buildHeatmap(props.history, props.weeks));

// Разбиваем на колонки по неделям (7 строк каждая)
const columns = computed(() => {
  const cols = [];
  for (let i = 0; i < cells.value.length; i += 7) {
    cols.push(cells.value.slice(i, i + 7));
  }
  return cols;
});

const levelClasses = [
  "bg-white/5 border-white/10",
  "bg-accent/15 border-accent/20",
  "bg-accent/30 border-accent/30",
  "bg-accent/50 border-accent/40",
  "bg-accent/80 border-accent/60",
];

function cellTitle(cell) {
  const d = new Date(cell.date).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
  });
  return `${d} — ${cell.count} сессий`;
}
</script>

<template>
  <div class="relative">
    <div class="flex gap-1 overflow-x-auto pb-2">
      <div
        v-for="(col, ci) in columns"
        :key="ci"
        class="flex flex-col gap-1"
      >
        <div
          v-for="cell in col"
          :key="cell.date"
          :title="cellTitle(cell)"
          class="w-3.5 h-3.5 rounded-[3px] border transition
                 hover:ring-2 hover:ring-accent/40 hover:scale-110"
          :class="levelClasses[levelFor(cell.count)]"
          @mouseenter="hovered = cell"
          @mouseleave="hovered = null"
        />
      </div>
    </div>

    <div class="flex items-center justify-between mt-3 text-xs text-muted">
      <span>Активность за {{ weeks }} недель</span>
      <div class="flex items-center gap-1.5">
        <span>меньше</span>
        <div
          v-for="i in 5"
          :key="i"
          class="w-3 h-3 rounded-[3px] border"
          :class="levelClasses[i - 1]"
        />
        <span>больше</span>
      </div>
    </div>

    <transition name="fade">
      <div
        v-if="hovered"
        class="absolute -top-9 left-0 bg-panel2 border border-white/10
               rounded-lg px-2.5 py-1 text-xs text-white shadow-lg
               pointer-events-none whitespace-nowrap"
      >
        {{ cellTitle(hovered) }}
      </div>
    </transition>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>