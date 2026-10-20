<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import InstallPrompt from "@/components/InstallPrompt.vue";
import NetworkStatus from "@/components/NetworkStatus.vue";
import AchievementToast from "@/components/AchievementToast.vue";

const auth = useAuthStore();
const router = useRouter();

onMounted(async () => {
  if (auth.isAuthenticated && !auth.user) {
    try {
      await auth.fetchMe();
    } catch {
      auth.logout();
      router.push("/login");
    }
  }
});
</script>

<template>
  <NetworkStatus />
  <router-view />
  <InstallPrompt />
  <AchievementToast />
</template>