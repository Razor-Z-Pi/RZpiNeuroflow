<script setup>
import { ref, computed, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import AppIcon from "@/components/AppIcon.vue";

const auth = useAuthStore();
const router = useRouter();

const step = ref(1); // 1=welcome, 2=reading, 3=memory, 4=result

// --- Чтение ---
const READING_TEXT = `Память работает как мышечная ткань: без нагрузки слабеет, с нагрузкой растёт. Главное правило тренировки — регулярность важнее интенсивности. Пятнадцать минут каждый день дают больше, чем три часа раз в неделю. Это подтверждается и в исследованиях нейропластичности, и в практике скорочтения.`;

const readingPhase = ref("ready"); // ready | running | done
const readingStart = ref(0);
const readingElapsed = ref(0);
const readingTimer = ref(null);
const comprehension = ref(70);
const wordCount = computed(() => READING_TEXT.trim().split(/\s+/).length);
const readingWpm = computed(() =>
  readingElapsed.value > 0
    ? Math.round((wordCount.value / readingElapsed.value) * 60)
    : 0
);

function startReading() {
  readingPhase.value = "running";
  readingStart.value = Date.now();
  readingTimer.value = setInterval(() => {
    readingElapsed.value = Math.floor((Date.now() - readingStart.value) / 1000);
  }, 200);
}

function finishReading() {
  clearInterval(readingTimer.value);
  if (readingElapsed.value === 0) readingElapsed.value = 1;
  readingPhase.value = "done";
}

// --- Память ---
const MEMORY_WORDS = [
  "яблоко", "стол", "лес", "ключ", "облако",
  "мост", "лампа", "река", "письмо", "тигр",
];

const memoryPhase = ref("ready"); // ready | showing | input | done
const memoryIndex = ref(0);
const memoryInput = ref("");
const memoryResult = ref([]);
const memoryTimer = ref(null);

function startMemory() {
  memoryIndex.value = 0;
  memoryInput.value = "";
  memoryResult.value = [];
  memoryPhase.value = "showing";

  memoryTimer.value = setInterval(() => {
    memoryIndex.value += 1;
    if (memoryIndex.value >= MEMORY_WORDS.length) {
      clearInterval(memoryTimer.value);
      memoryPhase.value = "input";
    }
  }, 1500);
}

function checkMemory() {
  const tokens = memoryInput.value
    .toLowerCase()
    .split(/[\s,;]+/)
    .map((w) => w.trim())
    .filter(Boolean);
  memoryResult.value = MEMORY_WORDS.map((w) => ({
    word: w,
    hit: tokens.includes(w.toLowerCase()),
  }));
  memoryPhase.value = "done";
}

const memoryHits = computed(
  () => memoryResult.value.filter((r) => r.hit).length
);

// --- Финал ---
const saving = ref(false);

async function saveBaseline() {
  saving.value = true;
  try {
    await auth.saveBaseline({
      baseline_wpm: readingWpm.value,
      baseline_comprehension: comprehension.value,
      baseline_memory: memoryHits.value,
    });
    step.value = 4;
  } finally {
    saving.value = false;
  }
}

function goToDashboard() {
  router.push("/");
}

onUnmounted(() => {
  clearInterval(readingTimer.value);
  clearInterval(memoryTimer.value);
});
</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-12 relative overflow-hidden">
    <div class="pointer-events-none absolute -top-40 -left-40 w-[420px] h-[420px] rounded-full bg-violet/15 blur-[120px]" />
    <div class="pointer-events-none absolute -bottom-40 -right-40 w-[420px] h-[420px] rounded-full bg-accent/10 blur-[120px]" />

    <div class="card w-full max-w-xl relative animate-fade-up">
      <!-- Индикатор шагов -->
      <div v-if="step < 4" class="flex items-center gap-2 mb-6">
        <div
          v-for="s in 3"
          :key="s"
          class="h-1 flex-1 rounded-full transition"
          :class="s <= step ? 'bg-accent' : 'bg-white/10'"
        />
      </div>

      <!-- ШАГ 1: Приветствие -->
      <div v-if="step === 1">
        <div class="w-14 h-14 rounded-2xl bg-accent/15 border border-accent/30
                    flex items-center justify-center text-accent mb-5">
          <AppIcon name="brain" :size="28" />
        </div>
        <h1 class="text-2xl font-bold mb-2">Добро пожаловать, {{ auth.user?.username }}</h1>
        <p class="text-muted mb-6">
          Прежде чем начать, замерим твою точку отсчёта. Это займёт 2 минуты.
          Дальше все результаты будут сравниваться с этим baseline — и ты
          увидишь реальный рост, а не абстрактные баллы.
        </p>
        <ul class="space-y-2 mb-6 text-sm text-muted">
          <li class="flex items-center gap-2">
            <AppIcon name="check" :size="14" class="text-accent" />
            Короткий текст на скорость чтения
          </li>
          <li class="flex items-center gap-2">
            <AppIcon name="check" :size="14" class="text-accent" />
            10 слов на память
          </li>
        </ul>
        <button class="btn-primary w-full" @click="step = 2">
          Поехали
        </button>
      </div>

      <!-- ШАГ 2: Чтение -->
      <div v-else-if="step === 2">
        <p class="label mb-1">Шаг 1 из 2 · Чтение</p>
        <h2 class="text-xl font-bold mb-2">Замер скорости</h2>

        <template v-if="readingPhase === 'ready'">
          <p class="text-muted mb-6">
            Прочитай текст ниже в своём обычном темпе. Жми «Старт», потом
            «Готово», когда дочитаешь.
          </p>
          <button class="btn-primary" @click="startReading">Старт</button>
        </template>

        <template v-else-if="readingPhase === 'running'">
          <div class="flex justify-between items-center mb-4 text-sm">
            <p class="text-muted">Идёт чтение</p>
            <p class="text-accent font-mono">{{ readingElapsed }} с</p>
          </div>
          <p class="leading-relaxed text-base mb-6 select-none">{{ READING_TEXT }}</p>
          <button class="btn-primary" @click="finishReading">Готово</button>
        </template>

        <template v-else>
          <div class="grid grid-cols-2 gap-3 mb-5">
            <div class="bg-panel2 rounded-xl p-3 border border-white/5">
              <p class="label mb-1">Скорость</p>
              <p class="text-xl font-bold text-accent">{{ readingWpm }} <span class="text-xs text-muted">wpm</span></p>
            </div>
            <div class="bg-panel2 rounded-xl p-3 border border-white/5">
              <p class="label mb-1">Время</p>
              <p class="text-xl font-bold">{{ readingElapsed }} <span class="text-xs text-muted">с</span></p>
            </div>
          </div>
          <label class="label block mb-2">
            Понимание: <span class="text-accent">{{ comprehension }}%</span>
          </label>
          <input
            v-model.number="comprehension"
            type="range"
            min="0"
            max="100"
            step="5"
            class="w-full accent-accent mb-6"
          />
          <button class="btn-primary w-full" @click="step = 3">Дальше</button>
        </template>
      </div>

      <!-- ШАГ 3: Память -->
      <div v-else-if="step === 3">
        <p class="label mb-1">Шаг 2 из 2 · Память</p>
        <h2 class="text-xl font-bold mb-2">Замер памяти</h2>

        <template v-if="memoryPhase === 'ready'">
          <p class="text-muted mb-6">
            Появятся 10 слов по одному. Представь каждое как яркий образ.
            Потом впиши всё, что запомнил.
          </p>
          <button class="btn-primary" @click="startMemory">Старт</button>
        </template>

        <template v-else-if="memoryPhase === 'showing'" class="text-center py-10 block">
          <p class="label mb-4">{{ memoryIndex + 1 }} / {{ MEMORY_WORDS.length }}</p>
          <transition name="word" mode="out-in">
            <p :key="memoryIndex" class="text-4xl font-bold text-accent">
              {{ MEMORY_WORDS[memoryIndex] }}
            </p>
          </transition>
        </template>

        <template v-else-if="memoryPhase === 'input'">
          <p class="text-muted mb-4">Что запомнил? Через запятую или пробел.</p>
          <textarea
            v-model="memoryInput"
            rows="3"
            class="input resize-none mb-4"
            placeholder="яблоко, стол, лес..."
          />
          <button class="btn-primary w-full" @click="checkMemory">Проверить</button>
        </template>

        <template v-else>
          <p class="text-2xl font-bold mb-4">
            Запомнено <span class="text-accent">{{ memoryHits }}</span> из {{ MEMORY_WORDS.length }}
          </p>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 mb-6">
            <div
              v-for="r in memoryResult"
              :key="r.word"
              class="rounded-lg px-2 py-1.5 text-xs border flex items-center gap-1.5"
              :class="r.hit
                ? 'bg-accent/10 border-accent/30 text-accent'
                : 'bg-red-500/10 border-red-500/30 text-red-300'"
            >
              <AppIcon v-if="r.hit" name="check" :size="12" />
              <span v-else>—</span>
              {{ r.word }}
            </div>
          </div>
          <button class="btn-primary w-full" :disabled="saving" @click="saveBaseline">
            {{ saving ? "Сохраняем..." : "Сохранить точку отсчёта" }}
          </button>
        </template>
      </div>

      <!-- ШАГ 4: Готово -->
      <div v-else class="text-center py-4">
        <div class="w-16 h-16 mx-auto rounded-full bg-accent/15 border border-accent/30
                    flex items-center justify-center text-accent mb-4">
          <AppIcon name="check" :size="32" />
        </div>
        <h2 class="text-xl font-bold mb-2">Точка отсчёта зафиксирована</h2>
        <p class="text-muted mb-6">
          Baseline: {{ auth.user?.baseline_wpm }} wpm,
          {{ auth.user?.baseline_comprehension }}% понимания,
          {{ auth.user?.baseline_memory }} элементов памяти.
        </p>
        <button class="btn-primary w-full" @click="goToDashboard">
          Перейти к тренировкам
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.word-enter-active,
.word-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.word-enter-from {
  opacity: 0;
  transform: translateY(6px);
}
.word-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>