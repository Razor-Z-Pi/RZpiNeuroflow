<script setup>
import { ref, computed, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useStatsStore } from "@/stores/stats";
import AppIcon from "@/components/AppIcon.vue";
import Hint from "@/components/Hint.vue";

const router = useRouter();
const stats = useStatsStore();

const TEXT = `Мозг — это не фиксированная величина, а живая система, которая меняется в ответ на нагрузку. Джим Квик в своих исследованиях показал: главные враги быстрого чтения — это внутреннее проговаривание и возвратные движения глаз. Если убрать эти две привычки, скорость чтения вырастает в полтора-два раза без потери понимания. Томас Франк дополняет эту картину: навык нужно деконструировать на компоненты и тренировать каждый отдельно, а затем собирать обратно. Это и есть осознанная практика. Простое повторение без обратной связи не даёт роста. А тренировка с замером результата и корректировкой подхода — даёт.`;

const phase = ref("ready"); // ready | running | done
const startTime = ref(0);
const elapsed = ref(0);
const comprehension = ref(75);
const submitting = ref(false);
const offlineSaved = ref(false);
const timer = ref(null);

const wordCount = computed(() => TEXT.trim().split(/\s+/).length);
const wpm = computed(() =>
  elapsed.value > 0 ? Math.round((wordCount.value / elapsed.value) * 60) : 0
);

function start() {
  phase.value = "running";
  startTime.value = Date.now();
  timer.value = setInterval(() => {
    elapsed.value = Math.floor((Date.now() - startTime.value) / 1000);
  }, 200);
}

function finish() {
  clearInterval(timer.value);
  if (elapsed.value === 0) elapsed.value = 1;
  phase.value = "done";
}

async function submit() {
  submitting.value = true;
  offlineSaved.value = false;
  try {
    const result = await stats.submitExercise({
      exercise_type: "reading",
      duration_sec: Math.max(elapsed.value, 1),
      accuracy: comprehension.value,
      speed_wpm: wpm.value,
      memory_items: 0,
      errors: 0,
    });

    if (result?.offline) {
      // Дадим баннеру оффлайн-очереди отрисоваться, потом уйдём
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
  elapsed.value = 0;
  comprehension.value = 75;
}

onUnmounted(() => clearInterval(timer.value));
</script>

<template>
  <div class="card animate-fade-up">
  <Hint
    hint-key="hint_reading"
    title="Как читать быстрее"
    text="Не проговаривай слова про себя и не возвращайся назад. Веди взглядом по строкам ровно и старайся охватывать больше слов за один фиксационный прыжок."
  />
    <!-- READY -->
    <div v-if="phase === 'ready'">
      <h2 class="text-xl font-bold mb-2">Скорочтение</h2>
      <p class="text-muted mb-6">
        Прочитай текст как можно быстрее, но сохрани понимание. Жми «Старт»,
        когда будешь готов, затем «Готово» — система замерит скорость.
      </p>
      <div class="text-sm text-muted mb-6 inline-flex items-center gap-2">
        <AppIcon name="reading" :size="14" />
        {{ wordCount }} слов в тексте
      </div>
      <button class="btn-primary" @click="start">Старт</button>
    </div>

    <!-- RUNNING -->
    <div v-else-if="phase === 'running'">
      <div class="flex items-center justify-between mb-4">
        <p class="text-muted text-sm">Идёт чтение</p>
        <p class="text-accent font-mono text-lg">{{ elapsed }} с</p>
      </div>
      <p class="leading-relaxed text-lg mb-8 select-none">{{ TEXT }}</p>
      <button class="btn-primary" @click="finish">Готово</button>
    </div>

    <!-- DONE -->
    <div v-else>
      <h2 class="text-xl font-bold mb-2">Результат</h2>
      <p class="text-muted mb-6">Проверь скорость и оцени понимание.</p>

      <div class="grid grid-cols-2 gap-4 mb-6">
        <div class="bg-panel2 rounded-xl p-4 border border-white/5">
          <p class="label mb-1">Время</p>
          <p class="text-2xl font-bold">{{ elapsed }} <span class="text-sm text-muted">с</span></p>
        </div>
        <div class="bg-panel2 rounded-xl p-4 border border-white/5">
          <p class="label mb-1">Скорость</p>
          <p class="text-2xl font-bold text-accent">{{ wpm }} <span class="text-sm text-muted">wpm</span></p>
        </div>
      </div>

      <div class="mb-6">
        <div class="flex justify-between mb-2">
          <label class="label">Понимание текста</label>
          <span class="text-sm font-semibold text-accent">{{ comprehension }}%</span>
        </div>
        <input
          v-model.number="comprehension"
          type="range"
          min="0"
          max="100"
          step="5"
          class="w-full accent-accent"
        />
        <p class="text-muted text-xs mt-2">
          Честно оцени, сколько смысла ты удержал. Скорость без понимания не считается.
        </p>
      </div>

      <div v-if="offlineSaved" class="text-sm text-yellow-400 mb-4">
        Нет сети — результат сохранён локально, отправим при подключении.
      </div>

      <div class="flex gap-3">
        <button class="btn-primary" :disabled="submitting" @click="submit">
          {{ submitting ? "Сохраняем..." : "Сохранить результат" }}
        </button>
        <button class="btn-ghost" @click="restart">Ещё раз</button>
      </div>
    </div>
  </div>
</template>