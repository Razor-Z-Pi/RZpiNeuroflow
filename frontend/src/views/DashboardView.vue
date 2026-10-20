<script setup>
import { onMounted, computed, ref } from "vue";
import { useStatsStore } from "@/stores/stats";
import { useAuthStore } from "@/stores/auth";
import api from "@/api/client";
import AppLayout from "@/components/AppLayout.vue";
import AppIcon from "@/components/AppIcon.vue";

const stats = useStatsStore();
const auth = useAuthStore();
const recommendation = ref(null);

const exercises = [
  { type: "reading", name: "Скорочтение", desc: "Пакетное чтение по Джиму Квику", icon: "reading", accent: "text-accent" },
  { type: "memory", name: "Дворец памяти", desc: "Метод локусов и визуализация", icon: "memory", accent: "text-violet" },
  { type: "attention", name: "Внимание", desc: "Таблицы Шульте, тест Струпа", icon: "attention", accent: "text-yellow-400" },
  { type: "logic", name: "Мышление", desc: "Деконструкция навыка по Франку", icon: "logic", accent: "text-cyan-400" },
];

function delta(current, base) {
  if (!base) return null;
  const diff = Math.round(current - base);
  return diff;
}

const metrics = computed(() => {
  const s = stats.stats;
  const u = auth.user;
  return [
    {
      label: "Скорость",
      value: s?.avg_wpm ?? 0,
      unit: "wpm",
      delta: delta(s?.avg_wpm ?? 0, u?.baseline_wpm ?? 0),
    },
    {
      label: "Точность",
      value: s?.avg_accuracy ?? 0,
      unit: "%",
      delta: delta(s?.avg_accuracy ?? 0, u?.baseline_comprehension ?? 0),
    },
    {
      label: "Память",
      value: s?.best_memory ?? 0,
      unit: "эл.",
      delta: delta(s?.best_memory ?? 0, u?.baseline_memory ?? 0),
    },
    {
      label: "Стрик",
      value: s?.streak_days ?? 0,
      unit: "дн.",
      icon: "flame",
    },
  ];
});

const recommendedExercise = computed(() => {
  if (!recommendation.value) return null;
  return exercises.find((e) => e.type === recommendation.value.recommended_type);
});

async function loadRecommendation() {
  try {
    const { data } = await api.get("/api/stats/recommendation");
    recommendation.value = data;
  } catch {
    recommendation.value = null;
  }
}

onMounted(async () => {
  await stats.fetch();
  await loadRecommendation();
});
</script>

<template>
  <AppLayout>
    <section
      v-if="recommendedExercise"
      class="card mb-6 border-accent/30 bg-accent/5 animate-fade-up"
    >
      <div class="flex items-center gap-4">
        <div
          class="w-14 h-14 shrink-0 rounded-2xl bg-accent/15 border border-accent/30
                 flex items-center justify-center text-accent"
        >
          <AppIcon :name="recommendedExercise.icon" :size="26" />
        </div>
        <div class="flex-1">
          <p class="label mb-1">Рекомендация дня</p>
          <h2 class="font-semibold text-lg mb-1">{{ recommendedExercise.name }}</h2>
          <p class="text-muted text-sm">
            {{
              recommendation.reason === "not_trained"
                ? "Ты ещё не пробовал этот тип тренировки — самое время."
                : `Средний балл здесь ниже остальных (${recommendation.avg_score}). Подтянем?`
            }}
          </p>
        </div>
        <router-link
          :to="`/exercise/${recommendedExercise.type}`"
          class="btn-primary !py-2.5 !px-5 text-sm shrink-0"
        >
          Начать
        </router-link>
      </div>
    </section>

    <!-- Метрики с дельтой -->
    <section class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
      <div
        v-for="(m, i) in metrics"
        :key="m.label"
        class="card animate-fade-up"
        :style="{ animationDelay: `${i * 60}ms` }"
      >
        <div class="flex items-center justify-between mb-3">
          <p class="label">{{ m.label }}</p>
          <AppIcon v-if="m.icon === 'flame'" name="flame" :size="16" class="text-orange-400" />
        </div>
        <p class="text-3xl font-bold leading-none">
          {{ m.value }}
          <span class="text-sm text-muted font-medium ml-1">{{ m.unit }}</span>
        </p>
        <p
          v-if="m.delta !== null && m.delta !== undefined"
          class="text-xs mt-2 inline-flex items-center gap-1"
          :class="m.delta >= 0 ? 'text-accent' : 'text-red-400'"
        >
          <AppIcon name="trend-up" :size="12" :class="m.delta < 0 ? 'rotate-180' : ''" />
          {{ m.delta > 0 ? "+" : "" }}{{ m.delta }} от baseline
        </p>
      </div>
    </section>

    <!-- Тренировки -->
    <section>
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold">Тренировки</h2>
        <p class="text-muted text-xs">
          Сессий всего: {{ stats.stats?.total_sessions ?? 0 }}
        </p>
      </div>

      <div class="grid md:grid-cols-2 gap-4">
        <router-link
          v-for="(ex, i) in exercises"
          :key="ex.type"
          :to="`/exercise/${ex.type}`"
          class="card group hover:border-accent/40 hover:bg-panel2
                 transition-all cursor-pointer animate-fade-up
                 relative overflow-hidden"
          :style="{ animationDelay: `${i * 70}ms` }"
        >
          <div class="flex items-start gap-4">
            <div
              class="w-12 h-12 shrink-0 rounded-xl bg-white/5 border border-white/10
                     flex items-center justify-center transition
                     group-hover:border-accent/30 group-hover:bg-accent/5"
              :class="ex.accent"
            >
              <AppIcon :name="ex.icon" :size="22" />
            </div>
            <div class="flex-1">
              <h3 class="font-semibold mb-1 transition" :class="ex.accent">
                {{ ex.name }}
              </h3>
              <p class="text-muted text-sm">{{ ex.desc }}</p>
            </div>
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              class="text-muted group-hover:text-accent transition
                     group-hover:translate-x-1 mt-1"
            >
              <path d="M9 18l6-6-6-6" />
            </svg>
          </div>
        </router-link>
      </div>
    </section>

    <!-- Подсказка новичку -->
    <section
      v-if="!stats.stats || stats.stats.total_sessions === 0"
      class="card mt-6 border-accent/20 bg-accent/5 animate-fade-up"
    >
      <div class="flex items-start gap-3">
        <AppIcon name="check" :size="20" class="text-accent mt-0.5 shrink-0" />
        <div>
          <h3 class="font-semibold mb-1">Начни с короткой сессии</h3>
          <p class="text-muted text-sm">
            Достаточно 5 минут в день, чтобы запустить прогресс. Выбери любой
            тренажёр выше — система сама посчитает результат.
          </p>
        </div>
      </div>
    </section>
  </AppLayout>
</template>