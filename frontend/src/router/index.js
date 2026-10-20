import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
  { path: "/login", component: () => import("@/views/LoginView.vue") },
  {
    path: "/onboarding",
    component: () => import("@/views/OnboardingView.vue"),
    meta: { auth: true },
  },
  {
    path: "/",
    component: () => import("@/views/DashboardView.vue"),
    meta: { auth: true },
  },
  {
    path: "/exercise/:type",
    component: () => import("@/views/ExerciseView.vue"),
    meta: { auth: true },
  },
  {
    path: "/stats",
    component: () => import("@/views/StatsView.vue"),
    meta: { auth: true },
  },
  {
    path: "/settings",
    component: () => import("@/views/SettingsView.vue"),
    meta: { auth: true },
  },
  {
    path: "/achievements",
    component: () => import("@/views/AchievementsView.vue"),
    meta: { auth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();

  if (to.meta.auth && !auth.isAuthenticated) return "/login";

  if (to.meta.auth && auth.isAuthenticated && !auth.user) {
    try {
      await auth.fetchMe();
    } catch {
      auth.logout();
      return "/login";
    }
  }

  // Если пользователь авторизован, но не прошёл baseline —
  // отправляем на онбординг с любого авторизованного экрана
  if (
    auth.isAuthenticated &&
    auth.user &&
    auth.user.baseline_wpm === 0 &&
    to.path !== "/onboarding" &&
    to.path !== "/login"
  ) {
    return "/onboarding";
  }

  // С онбординга нельзя попасть, если baseline уже есть
  if (
    to.path === "/onboarding" &&
    auth.user &&
    auth.user.baseline_wpm > 0
  ) {
    return "/";
  }

  if (to.path === "/login" && auth.isAuthenticated) return "/";
});

export default router;