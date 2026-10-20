<script setup>
import { ref, computed, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useStatsStore } from "@/stores/stats";
import AppIcon from "@/components/AppIcon.vue";
import Hint from "@/components/Hint.vue";

const router = useRouter();
const stats = useStatsStore();

const phase = ref("ready"); // ready | running | done
const cells = ref([]);
const next = ref(1);
const errors = ref(0);
const startTime = ref(0);
const elapsed = ref(0);
const timer = ref(null);
const submitting = ref(false);
const offlineSaved = ref(false);

const total = 25;

const progress = computed(() =>
  Math.round(((next.value - 1) / total) * 100)
);

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function start() {
  const nums = shuffle(Array.from({ length: total }, (_, i) => i + 1));
  cells.value = nums.map((n) => ({ n, done: false, shake: false }));
  next.value = 1;
  errors.value = 0;
  elapsed.value = 0;
  offlineSaved.value = false;
  startTime.value = Date.now();
  phase.value = "running";

  timer.value = setInterval(() => {
    elapsed.value = Math.floor((Date.now() - startTime.value) / 1000);
  }, 200);
}

function click(cell) {
  if (phase.value !== "running" || cell.done) return;
  if (cell.n === next.value) {
    cell.done = true;
    next.value += 1;
    if (next.value > total) finish();
  } else {
    errors.value += 1;
    cell.shake = true;
    setTimeout(() => (cell.shake = false), 300);
  }
}

function finish() {
  clearInterval(timer.value);
  phase.value = "done";
}

async function submit() {
  submitting.value = true;
  offlineSaved.value = false;
  try {
    const totalClicks = total + errors.value;
    const accuracy = totalClicks > 0
      ? Math.round((total / totalClicks) * 100)
      : 100;

    const result = await stats.submitExercise({
      exercise_type: "attention",
      duration_sec: Math.max(elapsed.value, 1),
      accuracy,
      speed_wpm: 0,
      memory_items: 0,
      errors: errors.value,
    });

    if (result?.offline) {
      offlineSaved.value = true;
      await new Promise((r) => setTimeout(r, 700));
    }
    router.push("/");
  } finally {
    submitting.value = false;
  }
}

function restart() {
  clearInterval(timer.value);
  phase.value = "ready";
}

onUnmounted(() => clearInterval(timer.value));
</script>

<template>
  <div class="card animate-fade-up">
  <Hint
    hint-key="hint_attention"
    title="Таблица Шульте"
    text="Держи взгляд в центре таблицы, не води глазами по каждой цифре. Так тренируется периферическое зрение и расширяется поле внимания."
  />
    <!-- READY -->
    <div v-if="phase === 'ready'">
      <h2 class="text-xl font-bold mb-2">Таблица Шульте</h2>
      <p class="text-muted mb-6">
        Нажми все числа от 1 до 25 по порядку как можно быстрее. Смотри в центр
        таблицы, не води глазами по каждой цифре — так тренируется периферическое зрение.
      </p>
      <button class="btn-primary" @click="start">Старт</button>
    </div>

    <!-- RUNNING -->
    <div v-else-if="phase === 'running'">
      <div class="flex justify-between items-center mb-4 text-sm">
        <p class="text-muted">
          Следующее: <span class="text-accent font-bold text-base">{{ next }}</span>
        </p>
        <div class="flex gap-4">
          <p class="text-muted">Ошибок: <span class="text-red-400 font-semibold">{{ errors }}</span></p>
          <p class="text-accent font-mono">{{ elapsed }} с</p>
        </div>
      </div>

      <div class="w-full h-1 bg-white/5 rounded-full mb-6 overflow-hidden">
        <div
          class="h-full bg-accent transition-all duration-300"
          :style="{ width: progress + '%' }"
        />
      </div>

      <div class="grid grid-cols-5 gap-2 max-w-md mx-auto">
        <button
          v-for="cell in cells"
          :key="cell.n"
          class="aspect-square rounded-xl border text-lg font-bold transition
                 flex items-center justify-center"
          :class="[
            cell.done
              ? 'bg-accent/10 border-accent/30 text-accent/50'
              : 'bg-panel2 border-white/10 text-white hover:border-accent/50 hover:bg-panel2',
            cell.shake ? 'animate-shake border-red-500/60' : '',
          ]"
          :disabled="cell.done"
          @click="click(cell)"
        >
          {{ cell.n }}
        </button>
      </div>
    </div>

    <!-- DONE -->
    <div v-else class="text-center py-6">
      <div
        class="w-16 h-16 mx-auto rounded-full bg-accent/15 border border-accent/30
               flex items-center justify-center text-accent mb-4 animate-fade-up"
      >
        <AppIcon name="check" :size="30" />
      </div>
      <h2 class="text-xl font-bold mb-2">Готово</h2>
      <p class="text-muted mb-6">
        Время: <span class="text-accent font-bold">{{ elapsed }} с</span>,
        ошибок: <span class="text-red-400 font-semibold">{{ errors }}</span>
      </p>

      <div v-if="offlineSaved" class="text-sm text-yellow-400 mb-4">
        Нет сети — результат сохранён локально, отправим при подключении.
      </div>

      <div class="flex gap-3 justify-center">
        <button class="btn-primary" :disabled="submitting" @click="submit">
          {{ submitting ? "Сохраняем..." : "Сохранить результат" }}
        </button>
        <button class="btn-ghost" @click="restart">Ещё раз</button>
      </div>
    </div>
  </div>
</template>