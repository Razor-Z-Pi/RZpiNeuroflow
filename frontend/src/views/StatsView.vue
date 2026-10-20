<script setup>
import { onMounted, computed, ref } from "vue";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  RadialLinearScale,
  ArcElement,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line, Bar, Radar } from "vue-chartjs";
import { useStatsStore } from "@/stores/stats";
import { useAuthStore } from "@/stores/auth";
import AppLayout from "@/components/AppLayout.vue";
import AppIcon from "@/components/AppIcon.vue";
import Heatmap from "@/components/Heatmap.vue";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  RadialLinearScale,
  ArcElement,
  Tooltip,
  Legend,
  Filler
);

const stats = useStatsStore();
const auth = useAuthStore();
const exporting = ref(false);

const chartColors = {
  accent: "#B4FF39",
  violet: "#8B7BFF",
  yellow: "#F5C542",
  cyan: "#3FC9D6",
  muted: "#8892A6",
};

const typeLabels = {
  reading: "Чтение",
  memory: "Память",
  attention: "Внимание",
  logic: "Мышление",
};

const typeColors = {
  reading: chartColors.accent,
  memory: chartColors.violet,
  attention: chartColors.yellow,
  logic: chartColors.cyan,
};

onMounted(() => stats.fetch());

const history = computed(() => stats.stats?.history ?? []);

// --- Сводные карточки ---
const summary = computed(() => {
  const s = stats.stats;
  return [
    {
      label: "Всего сессий",
      value: s?.total_sessions ?? 0,
      unit: "",
    },
    {
      label: "Стрик",
      value: s?.streak_days ?? 0,
      unit: "дн.",
      accent: true,
    },
    {
      label: "Средняя скорость",
      value: s?.avg_wpm ?? 0,
      unit: "wpm",
    },
    {
      label: "Лучшая память",
      value: s?.best_memory ?? 0,
      unit: "эл.",
    },
  ];
});

// --- Линейный график: скорость чтения по датам ---
const readingPoints = computed(() =>
  history.value.filter((h) => h.type === "reading")
);

const lineData = computed(() => {
  const points = readingPoints.value;
  return {
    labels: points.map((p) =>
      new Date(p.date).toLocaleDateString("ru-RU", { day: "numeric", month: "short" })
    ),
    datasets: [
      {
        label: "Скорость (wpm)",
        data: points.map((p) => p.wpm),
        borderColor: chartColors.accent,
        backgroundColor: "rgba(180, 255, 57, 0.12)",
        tension: 0.35,
        fill: true,
        pointRadius: 3,
        pointHoverRadius: 5,
        pointBackgroundColor: chartColors.accent,
      },
    ],
  };
});

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: "#131A2A",
      borderColor: "rgba(255,255,255,0.1)",
      borderWidth: 1,
      padding: 10,
      titleColor: "#fff",
      bodyColor: "#B4FF39",
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: chartColors.muted, font: { size: 11 } },
    },
    y: {
      grid: { color: "rgba(255,255,255,0.05)" },
      ticks: { color: chartColors.muted, font: { size: 11 } },
    },
  },
};

// --- Столбчатая: количество сессий по типам ---
const barData = computed(() => {
  const counts = { reading: 0, memory: 0, attention: 0, logic: 0 };
  for (const h of history.value) {
    if (counts[h.type] !== undefined) counts[h.type] += 1;
  }
  return {
    labels: Object.keys(counts).map((k) => typeLabels[k]),
    datasets: [
      {
        label: "Сессий",
        data: Object.keys(counts).map((k) => counts[k]),
        backgroundColor: Object.keys(counts).map((k) => typeColors[k] + "80"),
        borderColor: Object.keys(counts).map((k) => typeColors[k]),
        borderWidth: 1.5,
        borderRadius: 8,
      },
    ],
  };
});

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: "#131A2A",
      borderColor: "rgba(255,255,255,0.1)",
      borderWidth: 1,
      padding: 10,
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: chartColors.muted, font: { size: 11 } },
    },
    y: {
      beginAtZero: true,
      grid: { color: "rgba(255,255,255,0.05)" },
      ticks: { color: chartColors.muted, stepSize: 1, font: { size: 11 } },
    },
  },
};

// --- Радар: средний балл по типам ---
const radarData = computed(() => {
  const sums = { reading: [], memory: [], attention: [], logic: [] };
  for (const h of history.value) {
    if (sums[h.type]) sums[h.type].push(h.score);
  }
  const avgs = Object.keys(sums).map((k) => {
    const arr = sums[k];
    return arr.length ? Math.round(arr.reduce((a, b) => a + b, 0) / arr.length) : 0;
  });
  return {
    labels: Object.keys(sums).map((k) => typeLabels[k]),
    datasets: [
      {
        label: "Средний балл",
        data: avgs,
        backgroundColor: "rgba(139, 123, 255, 0.18)",
        borderColor: chartColors.violet,
        borderWidth: 2,
        pointBackgroundColor: chartColors.violet,
        pointRadius: 4,
      },
    ],
  };
});

const radarOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: "#131A2A",
      borderColor: "rgba(255,255,255,0.1)",
      borderWidth: 1,
      padding: 10,
    },
  },
  scales: {
    r: {
      min: 0,
      max: 100,
      angleLines: { color: "rgba(255,255,255,0.08)" },
      grid: { color: "rgba(255,255,255,0.08)" },
      pointLabels: { color: "#fff", font: { size: 12, weight: "600" } },
      ticks: {
        color: chartColors.muted,
        backdropColor: "transparent",
        stepSize: 25,
        font: { size: 9 },
      },
    },
  },
};

// --- Последние сессии ---
const recent = computed(() => [...history.value].reverse().slice(0, 8));

async function handleExport() {
  exporting.value = true;
  try {
    await stats.exportCsv();
  } finally {
    exporting.value = false;
  }
}
</script>

<template>
  <AppLayout>
    <div v-if="stats.loading" class="text-center text-muted py-20">
      Загрузка статистики...
    </div>

    <div v-else-if="!history.length" class="card text-center py-12 animate-fade-up">
      <div
        class="w-16 h-16 mx-auto rounded-full bg-accent/15 border border-accent/30
               flex items-center justify-center text-accent mb-4"
      >
        <AppIcon name="chart" :size="30" />
      </div>
      <h2 class="text-lg font-bold mb-2">Пока нет данных</h2>
      <p class="text-muted mb-6">
        Пройди первую тренировку, чтобы увидеть график прогресса.
      </p>
      <router-link to="/" class="btn-primary inline-block">К тренировкам</router-link>
    </div>

    <template v-else>
      <!-- Сводные карточки -->
      <section class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div
          v-for="(s, i) in summary"
          :key="s.label"
          class="card animate-fade-up"
          :style="{ animationDelay: `${i * 60}ms` }"
        >
          <p class="label mb-2">{{ s.label }}</p>
          <p
            class="text-3xl font-bold leading-none"
            :class="s.accent ? 'text-accent' : ''"
          >
            {{ s.value }}
            <span class="text-sm text-muted font-medium ml-1">{{ s.unit }}</span>
          </p>
        </div>
      </section>

      <!-- График скорости чтения -->
      <section class="card mb-6 animate-fade-up">
        <div class="flex justify-between items-center mb-5">
          <div>
            <h2 class="text-lg font-semibold">Скорость чтения</h2>
            <p class="text-muted text-xs mt-1">
              Динамика слов в минуту по сессиям
            </p>
          </div>
          <button
            class="btn-ghost !py-2 !px-3 text-xs inline-flex items-center gap-2"
            :disabled="exporting"
            @click="handleExport"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <path d="M7 10l5 5 5-5" />
              <path d="M12 15V3" />
            </svg>
            {{ exporting ? "Готовим..." : "CSV" }}
          </button>
        </div>
        <div v-if="readingPoints.length" class="h-64">
          <Line :data="lineData" :options="lineOptions" />
        </div>
        <p v-else class="text-muted text-sm py-10 text-center">
          Ещё не было сессий по скорочтению.
        </p>
      </section>

      <!-- Heatmap + Radar -->
      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <section class="card animate-fade-up">
          <h2 class="text-lg font-semibold mb-1">Активность</h2>
          <p class="text-muted text-xs mb-5">Каждая клетка — один день</p>
          <Heatmap :history="history" :weeks="26" />
        </section>

        <section class="card animate-fade-up">
          <h2 class="text-lg font-semibold mb-1">Профиль навыков</h2>
          <p class="text-muted text-xs mb-3">Средний балл по каждой категории</p>
          <div class="h-64">
            <Radar :data="radarData" :options="radarOptions" />
          </div>
        </section>
      </div>

      <!-- Сессии по типам -->
      <section class="card mb-6 animate-fade-up">
        <h2 class="text-lg font-semibold mb-1">Распределение тренировок</h2>
        <p class="text-muted text-xs mb-5">Количество сессий по навыкам</p>
        <div class="h-56">
          <Bar :data="barData" :options="barOptions" />
        </div>
      </section>

      <!-- Последние сессии -->
      <section class="card animate-fade-up">
        <h2 class="text-lg font-semibold mb-4">Последние тренировки</h2>
        <div class="space-y-2">
          <div
            v-for="(h, i) in recent"
            :key="i"
            class="flex items-center gap-3 px-3 py-2.5 rounded-xl
                   bg-panel2 border border-white/5 hover:border-white/10 transition"
          >
            <div
              class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0"
              :style="{ backgroundColor: typeColors[h.type] + '18', color: typeColors[h.type] }"
            >
              <AppIcon :name="h.type" :size="15" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium">{{ typeLabels[h.type] }}</p>
              <p class="text-muted text-xs">
                {{ new Date(h.date).toLocaleString("ru-RU", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }) }}
              </p>
            </div>
            <div class="text-right">
              <p class="text-sm font-bold" :style="{ color: typeColors[h.type] }">
                {{ Math.round(h.score) }}
              </p>
              <p class="text-muted text-xs">
                <span v-if="h.type === 'reading'">{{ h.wpm }} wpm</span>
                <span v-else-if="h.type === 'memory'">{{ h.memory }} эл.</span>
                <span v-else>{{ Math.round(h.accuracy) }}%</span>
              </p>
            </div>
          </div>
        </div>
      </section>
    </template>
  </AppLayout>
</template>