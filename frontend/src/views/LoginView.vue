<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import AppIcon from "@/components/AppIcon.vue";

const auth = useAuthStore();
const router = useRouter();

const mode = ref("login");
const form = ref({ email: "", username: "", password: "" });
const error = ref("");
const loading = ref(false);

function switchMode(m) {
  mode.value = m;
  error.value = "";
}

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    if (mode.value === "login") {
      await auth.login(form.value.email.trim(), form.value.password);
    } else {
      await auth.register(
        form.value.email.trim(),
        form.value.username.trim(),
        form.value.password
      );
    }
    router.push("/");
  } catch (e) {
    const detail = e.response?.data?.detail;
    if (Array.isArray(detail)) {
      error.value = detail.map((d) => d.msg).join(", ");
    } else {
      error.value = detail || "Что-то пошло не так. Попробуй ещё раз.";
    }
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
    <!-- Декоративные пятна на фоне -->
    <div
      class="pointer-events-none absolute -top-40 -left-40 w-[420px] h-[420px] rounded-full
             bg-violet/20 blur-[120px] animate-fade-up"
    />
    <div
      class="pointer-events-none absolute -bottom-40 -right-40 w-[420px] h-[420px] rounded-full
             bg-accent/10 blur-[120px] animate-fade-up"
    />

    <div class="card w-full max-w-md relative animate-fade-up">
      <!-- Логотип -->
      <div class="flex items-center gap-3 mb-8">
        <div
          class="w-11 h-11 rounded-xl bg-accent/15 border border-accent/30
                 flex items-center justify-center text-accent"
        >
          <AppIcon name="brain" :size="22" />
        </div>
        <div>
          <h1 class="text-2xl font-extrabold leading-none">
            Neuro<span class="text-accent">Flow</span>
          </h1>
          <p class="text-muted text-xs mt-1">Тренируй мозг. Отслеживай прогресс.</p>
        </div>
      </div>

      <!-- Переключатель -->
      <div class="flex bg-panel2 rounded-xl p-1 mb-5">
        <button
          class="flex-1 py-2 rounded-lg text-sm font-medium transition"
          :class="mode === 'login' ? 'bg-accent text-black' : 'text-muted hover:text-white'"
          @click="switchMode('login')"
        >
          Вход
        </button>
        <button
          class="flex-1 py-2 rounded-lg text-sm font-medium transition"
          :class="mode === 'register' ? 'bg-accent text-black' : 'text-muted hover:text-white'"
          @click="switchMode('register')"
        >
          Регистрация
        </button>
      </div>

      <form class="space-y-3" @submit.prevent="submit">
        <input
          v-model="form.email"
          type="email"
          placeholder="Email"
          class="input"
          autocomplete="email"
          required
        />
        <input
          v-if="mode === 'register'"
          v-model="form.username"
          type="text"
          placeholder="Username"
          class="input"
          autocomplete="username"
          minlength="3"
          required
        />
        <input
          v-model="form.password"
          type="password"
          placeholder="Пароль"
          class="input"
          :autocomplete="mode === 'login' ? 'current-password' : 'new-password'"
          minlength="6"
          required
        />

        <transition name="fade">
          <div
            v-if="error"
            class="text-red-400 text-sm bg-red-500/10 border border-red-500/20
                   rounded-xl px-3 py-2"
          >
            {{ error }}
          </div>
        </transition>

        <button type="submit" class="btn-primary w-full !py-3" :disabled="loading">
          <span v-if="!loading">
            {{ mode === "login" ? "Войти" : "Создать аккаунт" }}
          </span>
          <span v-else class="inline-flex items-center gap-2">
            <svg class="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" opacity="0.25" />
              <path d="M22 12a10 10 0 0 0-10-10" stroke="currentColor" stroke-width="3" stroke-linecap="round" />
            </svg>
            Загрузка
          </span>
        </button>
      </form>

      <p class="text-muted text-xs text-center mt-6">
        Минимум 6 символов в пароле, 3 символа в username.
      </p>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>