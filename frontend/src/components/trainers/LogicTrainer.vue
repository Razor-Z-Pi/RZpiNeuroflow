<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useStatsStore } from "@/stores/stats";
import AppIcon from "@/components/AppIcon.vue";
import Hint from "@/components/Hint.vue";

const router = useRouter();
const stats = useStatsStore();

const TASKS = [
  {
    question:
      "Все фломы умеют плавать. Некоторые фломы поют. Что точно верно?",
    options: [
      "Все поющие умеют плавать",
      "Некоторые поющие умеют плавать",
      "Все пловцы поют",
      "Ничего из перечисленного",
    ],
    correct: 1,
  },
  {
    question: "Если сегодня понедельник, какой день будет через 100 дней?",
    options: ["Вторник", "Среда", "Четверг", "Пятница"],
    correct: 1,
  },
  {
    question:
      "Книга дороже ручки на 100 рублей. Вместе они стоят 250 рублей. Сколько стоит ручка?",
    options: ["150", "125", "75", "50"],
    correct: 2,
  },
  {
    question:
      "Все математики — логики. Некоторые логики — философы. Что верно?",
    options: [
      "Все философы — математики",
      "Некоторые математики — философы",
      "Все логики — математики",
      "Ничего не следует точно",
    ],
    correct: 3,
  },
  {
    question: "Найди лишнее: квадрат, треугольник, круг, прямоугольник.",
    options: ["Квадрат", "Треугольник", "Круг", "Прямоугольник"],
    correct: 2,
  },
];

const phase = ref("ready"); // ready | running | done
const index = ref(0);
const selected = ref(null);
const answers = ref([]);
const startTime = ref(0);
const elapsed = ref(0);
const submitting = ref(false);
const offlineSaved = ref(false);

const current = computed(() => TASKS[index.value]);
const total = computed(() => TASKS.length);

function start() {
  index.value = 0;
  selected.value = null;
  answers.value = [];
  elapsed.value = 0;
  offlineSaved.value = false;
  startTime.value = Date.now();
  phase.value = "running";
}

function choose(i) {
  if (selected.value !== null) return;
  selected.value = i;
  answers.value.push({
    task: index.value,
    choice: i,
    correct: i === current.value.correct,
  });
}

function nextTask() {
  if (index.value + 1 >= total.value) {
    elapsed.value = Math.max(
      Math.floor((Date.now() - startTime.value) / 1000),
      1
    );
    phase.value = "done";
    return;
  }
  index.value += 1;
  selected.value = null;
}

async function submit() {
  submitting.value = true;
  offlineSaved.value = false;
  try {
    const hits = answers.value.filter((a) => a.correct).length;
    const accuracy = Math.round((hits / total.value) * 100);

    const result = await stats.submitExercise({
      exercise_type: "logic",
      duration_sec: elapsed.value,
      accuracy,
      speed_wpm: 0,
      memory_items: 0,
      errors: total.value - hits,
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
  phase.value = "ready";
}
</script>

<template>
  <div class="card animate-fade-up">
  <Hint
    hint-key="hint_logic"
    title="Логика без спешки"
    text="Читай условие дважды. В формулировках с «все», «некоторые», «точно» — ищи подвох. Быстрый ответ не значит верный."
  />
    <!-- READY -->
    <div v-if="phase === 'ready'">
      <h2 class="text-xl font-bold mb-2">Мышление</h2>
      <p class="text-muted mb-6">
        Пять коротких логических задач. Читай внимательно — формулировки
        с подвохом. Время фиксируется автоматически.
      </p>
      <button class="btn-primary" @click="start">Начать</button>
    </div>

    <!-- RUNNING -->
    <div v-else-if="phase === 'running'">
      <div class="flex justify-between items-center mb-4 text-sm">
        <p class="label">Задача {{ index + 1 }} из {{ total }}</p>
        <div class="w-32 h-1 bg-white/5 rounded-full overflow-hidden">
          <div
            class="h-full bg-accent transition-all duration-300"
            :style="{ width: ((index) / total) * 100 + '%' }"
          />
        </div>
      </div>

      <p class="text-lg font-medium mb-6 leading-snug">{{ current.question }}</p>

      <div class="space-y-2 mb-6">
        <button
          v-for="(opt, i) in current.options"
          :key="i"
          class="w-full text-left px-4 py-3 rounded-xl border transition"
          :class="[
            selected === null
              ? 'bg-panel2 border-white/10 hover:border-accent/50 hover:bg-panel2'
              : i === current.correct
              ? 'bg-accent/10 border-accent/40 text-accent'
              : i === selected
              ? 'bg-red-500/10 border-red-500/40 text-red-300'
              : 'bg-panel2 border-white/5 text-muted',
          ]"
          :disabled="selected !== null"
          @click="choose(i)"
        >
          {{ opt }}
        </button>
      </div>

      <button v-if="selected !== null" class="btn-primary" @click="nextTask">
        {{ index + 1 >= total ? "Завершить" : "Дальше" }}
      </button>
    </div>

    <!-- DONE -->
    <div v-else class="text-center py-6">
      <div
        class="w-16 h-16 mx-auto rounded-full bg-accent/15 border border-accent/30
               flex items-center justify-center text-accent mb-4"
      >
        <AppIcon name="check" :size="30" />
      </div>
      <h2 class="text-xl font-bold mb-2">
        {{ answers.filter(a => a.correct).length }} из {{ total }} верно
      </h2>
      <p class="text-muted mb-6">
        Точность:
        <span class="text-accent font-bold">
          {{ Math.round((answers.filter(a => a.correct).length / total) * 100) }}%
        </span>,
        время: {{ elapsed }} с
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