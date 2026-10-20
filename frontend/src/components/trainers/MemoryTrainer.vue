<script setup>
import { ref, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useStatsStore } from "@/stores/stats";
import AppIcon from "@/components/AppIcon.vue";
import Hint from "@/components/Hint.vue";

const router = useRouter();
const stats = useStatsStore();

const ALL_WORDS = [
  "лампа", "река", "ключ", "зонт", "поезд",
  "стекло", "тигр", "мост", "часы", "письмо",
  "вишня", "снег", "книга", "огонь", "птица",
];

const phase = ref("ready"); // ready | showing | input | done
const words = ref([]);
const currentIndex = ref(0);
const input = ref("");
const remembered = ref([]);
const submitted = ref(false);
const submitting = ref(false);
const offlineSaved = ref(false);
const timer = ref(null);

function start() {
  const shuffled = [...ALL_WORDS].sort(() => Math.random() - 0.5).slice(0, 10);
  words.value = shuffled;
  currentIndex.value = 0;
  input.value = "";
  remembered.value = [];
  submitted.value = false;
  offlineSaved.value = false;
  phase.value = "showing";

  timer.value = setInterval(() => {
    currentIndex.value += 1;
    if (currentIndex.value >= words.value.length) {
      clearInterval(timer.value);
      phase.value = "input";
    }
  }, 1500);
}

function check() {
  const raw = input.value.toLowerCase();
  const tokens = raw
    .split(/[\s,;]+/)
    .map((w) => w.trim())
    .filter(Boolean);
  remembered.value = words.value.map((w) => ({
    word: w,
    hit: tokens.includes(w.toLowerCase()),
  }));
  phase.value = "done";
}

async function submit() {
  submitting.value = true;
  offlineSaved.value = false;
  try {
    const hits = remembered.value.filter((r) => r.hit).length;
    const accuracy = Math.round((hits / words.value.length) * 100);

    const result = await stats.submitExercise({
      exercise_type: "memory",
      duration_sec: words.value.length * 2 + 30,
      accuracy,
      speed_wpm: 0,
      memory_items: hits,
      errors: words.value.length - hits,
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
    hint-key="hint_memory"
    title="Дворец памяти"
    text="Представляй каждое слово как яркий образ в знакомой комнате: лампа на столе, ключ в замке, зонт у двери. Чем нелепее — тем легче запомнить."
  />
    <!-- READY -->
    <div v-if="phase === 'ready'">
      <h2 class="text-xl font-bold mb-2">Дворец памяти</h2>
      <p class="text-muted mb-6">
        Сейчас появятся 10 слов по одному. Представь каждое как яркий образ
        в знакомой комнате — так их проще удержать. Потом впиши всё, что запомнил.
      </p>
      <button class="btn-primary" @click="start">Начать показ</button>
    </div>

    <!-- SHOWING -->
    <div v-else-if="phase === 'showing'" class="text-center py-12">
      <p class="label mb-4">Слово {{ currentIndex + 1 }} из {{ words.length }}</p>
      <transition name="word" mode="out-in">
        <p :key="currentIndex" class="text-5xl font-bold text-accent">
          {{ words[currentIndex] }}
        </p>
      </transition>
    </div>

    <!-- INPUT -->
    <div v-else-if="phase === 'input'">
      <h2 class="text-xl font-bold mb-2">Что запомнил?</h2>
      <p class="text-muted mb-6">
        Впиши слова через запятую или пробел. Порядок не важен.
      </p>
      <textarea
        v-model="input"
        rows="4"
        class="input resize-none font-mono text-base"
        placeholder="лампа, река, ключ..."
      ></textarea>
      <button class="btn-primary mt-4" @click="check">Проверить</button>
    </div>

    <!-- DONE -->
    <div v-else>
      <h2 class="text-xl font-bold mb-2">
        Запомнено {{ remembered.filter(r => r.hit).length }} из {{ words.length }}
      </h2>
      <p class="text-muted mb-6">Разбор по словам:</p>

      <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 mb-6">
        <div
          v-for="r in remembered"
          :key="r.word"
          class="rounded-lg px-3 py-2 text-sm border flex items-center gap-2"
          :class="r.hit
            ? 'bg-accent/10 border-accent/30 text-accent'
            : 'bg-red-500/10 border-red-500/30 text-red-300'"
        >
          <AppIcon v-if="r.hit" name="check" :size="14" />
          <span v-else class="text-xs">—</span>
          {{ r.word }}
        </div>
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

<style scoped>
.word-enter-active,
.word-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.word-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.word-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>