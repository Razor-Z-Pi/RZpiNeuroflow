<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import AppIcon from "@/components/AppIcon.vue";

const deferredPrompt = ref(null);
const visible = ref(false);

function onBeforeInstall(e) {
  e.preventDefault();
  deferredPrompt.value = e;
  if (!localStorage.getItem("nf_install_dismissed")) {
    visible.value = true;
  }
}

async function install() {
  if (!deferredPrompt.value) return;
  deferredPrompt.value.prompt();
  const { outcome } = await deferredPrompt.value.userChoice;
  if (outcome === "accepted") {
    visible.value = false;
  }
  deferredPrompt.value = null;
}

function dismiss() {
  visible.value = false;
  localStorage.setItem("nf_install_dismissed", "1");
}

onMounted(() => {
  window.addEventListener("beforeinstallprompt", onBeforeInstall);
});

onUnmounted(() => {
  window.removeEventListener("beforeinstallprompt", onBeforeInstall);
});
</script>

<template>
  <transition name="slide-up">
    <div
      v-if="visible"
      class="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-96
             card border-accent/30 bg-panel/95 backdrop-blur-md z-50
             shadow-2xl flex items-start gap-3"
    >
      <div
        class="w-10 h-10 shrink-0 rounded-xl bg-accent/15 border border-accent/30
               flex items-center justify-center text-accent"
      >
        <AppIcon name="brain" :size="20" />
      </div>
      <div class="flex-1 min-w-0">
        <p class="font-semibold text-sm mb-0.5">Установить NeuroFlow</p>
        <p class="text-muted text-xs mb-3">
          Добавь на главный экран — будет работать без сети.
        </p>
        <div class="flex gap-2">
          <button class="btn-primary !py-1.5 !px-3 text-xs" @click="install">
            Установить
          </button>
          <button class="btn-ghost !py-1.5 !px-3 text-xs" @click="dismiss">
            Позже
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>