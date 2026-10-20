<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useThemeStore } from "@/stores/theme";
import AppLayout from "@/components/AppLayout.vue";
import AppIcon from "@/components/AppIcon.vue";
import { resetAll as resetHintsAll } from "@/utils/hints";

function resetHints() {
  resetHintsAll();
  alert("Подсказки сброшены");
}

const auth = useAuthStore();
const theme = useThemeStore();
const router = useRouter();

// --- Пароль ---
const pw = ref({ current: "", next: "", confirm: "" });
const pwError = ref("");
const pwSuccess = ref(false);
const pwLoading = ref(false);

async function changePassword() {
  pwError.value = "";
  pwSuccess.value = false;
  if (pw.value.next !== pw.value.confirm) {
    pwError.value = "Новые пароли не совпадают";
    return;
  }
  if (pw.value.next.length < 6) {
    pwError.value = "Минимум 6 символов";
    return;
  }
  pwLoading.value = true;
  try {
    await auth.changePassword(pw.value.current, pw.value.next);
    pwSuccess.value = true;
    pw.value = { current: "", next: "", confirm: "" };
  } catch (e) {
    pwError.value = e.response?.data?.detail || "Ошибка";
  } finally {
    pwLoading.value = false;
  }
}

// --- Экспорт ---
const exporting = ref(false);
async function exportData() {
  exporting.value = true;
  try {
    await (await import("@/stores/stats")).useStatsStore().exportCsv();
  } finally {
    exporting.value = false;
  }
}

// --- Удаление ---
const deleteStep = ref(0); // 0=скрыто, 1=подтверждение, 2=ввод
const deleteInput = ref("");
const deleting = ref(false);

async function confirmDelete() {
  if (deleteInput.value !== auth.user?.username) return;
  deleting.value = true;
  try {
    await auth.deleteAccount();
    router.push("/login");
  } finally {
    deleting.value = false;
  }
}
</script>

<template>
  <AppLayout>
    <h1 class="text-2xl font-bold mb-6">Настройки</h1>

    <div class="grid md:grid-cols-2 gap-6">
      <!-- Профиль -->
      <section class="card animate-fade-up">
        <h2 class="font-semibold mb-4">Профиль</h2>
        <div class="space-y-3 text-sm">
          <div class="flex justify-between">
            <span class="text-muted">Username</span>
            <span class="font-medium">{{ auth.user?.username }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-muted">Email</span>
            <span class="font-medium">{{ auth.user?.email }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-muted">Регистрация</span>
            <span class="font-medium">
              {{ new Date(auth.user?.created_at).toLocaleDateString("ru-RU") }}
            </span>
          </div>
        </div>
      </section>

      <!-- Тема -->
      <section class="card animate-fade-up">
        <h2 class="font-semibold mb-4">Оформление</h2>
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium">Тема</p>
            <p class="text-muted text-xs mt-1">
              {{ theme.theme === "dark" ? "Тёмная" : "Светлая" }}
            </p>
          </div>
          <button class="btn-ghost !py-2 !px-4 text-sm inline-flex items-center gap-2" @click="theme.toggle()">
            <AppIcon :name="theme.theme === 'dark' ? 'sun' : 'moon'" :size="16" />
            Сменить
          </button>
        </div>
        <section class="card animate-fade-up">
                <h2 class="font-semibold mb-4">Подсказки</h2>
                <p class="text-muted text-sm mb-4">
                    Сбросить все подсказки в тренажёрах, чтобы увидеть их заново.
                </p>
                <button class="btn-ghost" @click="resetHints">
                    Показать подсказки заново
                </button>
          </section>
      </section>

      <!-- Смена пароля -->
      <section class="card animate-fade-up md:col-span-2">
        <h2 class="font-semibold mb-4">Смена пароля</h2>
        <form class="space-y-3 max-w-md" @submit.prevent="changePassword">
          <input
            v-model="pw.current"
            type="password"
            placeholder="Текущий пароль"
            class="input"
            required
          />
          <input
            v-model="pw.next"
            type="password"
            placeholder="Новый пароль"
            class="input"
            required
          />
          <input
            v-model="pw.confirm"
            type="password"
            placeholder="Повтори новый"
            class="input"
            required
          />
          <p v-if="pwError" class="text-red-400 text-sm">{{ pwError }}</p>
          <p v-if="pwSuccess" class="text-accent text-sm">Пароль изменён</p>
          <button type="submit" class="btn-primary" :disabled="pwLoading">
            {{ pwLoading ? "Сохраняем..." : "Изменить пароль" }}
          </button>
        </form>
      </section>

      <!-- Экспорт -->
      <section class="card animate-fade-up">
        <h2 class="font-semibold mb-4">Экспорт данных</h2>
        <p class="text-muted text-sm mb-4">
          Скачай историю всех тренировок в CSV: дата, тип, точность, скорость, память.
        </p>
        <button class="btn-ghost inline-flex items-center gap-2" :disabled="exporting" @click="exportData">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <path d="M7 10l5 5 5-5" />
            <path d="M12 15V3" />
          </svg>
          {{ exporting ? "Готовим..." : "Скачать CSV" }}
        </button>
      </section>

      <!-- Удаление -->
      <section class="card border-red-500/30 animate-fade-up">
        <h2 class="font-semibold mb-2 text-red-400">Удаление аккаунта</h2>
        <p class="text-muted text-sm mb-4">
          Все данные будут удалены безвозвратно: сессии, результаты, baseline.
        </p>
        <button
          v-if="deleteStep === 0"
          class="btn-ghost !text-red-400 !border-red-500/30"
          @click="deleteStep = 1"
        >
          Удалить аккаунт
        </button>

        <div v-else-if="deleteStep === 1" class="space-y-3">
          <p class="text-sm">
            Точно? Введи свой username
            <span class="font-mono text-red-300">{{ auth.user?.username }}</span>
            для подтверждения.
          </p>
          <input
            v-model="deleteInput"
            :placeholder="auth.user?.username"
            class="input"
          />
          <div class="flex gap-2">
            <button
              class="btn-ghost !text-red-400 !border-red-500/30"
              :disabled="deleteInput !== auth.user?.username || deleting"
              @click="confirmDelete"
            >
              {{ deleting ? "Удаляем..." : "Подтвердить удаление" }}
            </button>
            <button class="btn-ghost" @click="deleteStep = 0; deleteInput = ''">
              Отмена
            </button>
          </div>
        </div>
      </section>
    </div>
  </AppLayout>
</template>