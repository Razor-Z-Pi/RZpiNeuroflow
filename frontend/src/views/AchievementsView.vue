<script setup>
import { onMounted, computed, ref } from "vue";
import { useAchievementsStore } from "@/stores/achievements";
import AppLayout from "@/components/AppLayout.vue";
import AppIcon from "@/components/AppIcon.vue";

const store = useAchievementsStore();
const filter = ref("all"); // all | unlocked | locked

const filtered = computed(() => {
  if (filter.value === "unlocked") return store.unlocked;
  if (filter.value === "locked") return store.locked;
  return store.items;
});

const progressPercent = computed(() =>
  store.total ? Math.round((store.unlockedCount / store.total) * 100) : 0
);

onMounted(() => store.fetch());
</script>

<template>
  <AppLayout>
    <div class="flex items-start justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold">Достижения</h1>
        <p class="text-muted text-sm mt-1">
          {{ store.unlockedCount }} из {{ store.total }} открыто
        </p>
      </div>
      <div
        class="w-14 h-14 shrink-0 rounded-2xl bg-accent/15 border border-accent/30
               flex items-center justify-center text-accent"
      >
        <AppIcon name="trophy" :size="26" />
      </div>
    </div>

    <!-- Прогресс -->
    <div class="w-full h-2 bg-ink/5 rounded-full mb-6 overflow-hidden">
      <div
        class="h-full bg-accent transition-all duration-500"
        :style="{ width: progressPercent + '%' }"
      />
    </div>

    <!-- Фильтр -->
    <div class="flex gap-2 mb-6">
      <button
        v-for="f in [
          { id: 'all', label: 'Все' },
          { id: 'unlocked', label: 'Открытые' },
          { id: 'locked', label: 'Закрытые' },
        ]"
        :key="f.id"
        class="px-4 py-1.5 rounded-lg text-sm transition"
        :class="filter === f.id
          ? 'bg-accent text-black font-semibold'
          : 'bg-panel2 text-muted hover:text-ink'"
        @click="filter = f.id"
      >
        {{ f.label }}
      </button>
    </div>

    <div v-if="store.loading" class="text-center text-muted py-12">
      Загрузка...
    </div>

    <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="(a, i) in filtered"
        :key="a.code"
        class="card animate-fade-up relative overflow-hidden"
        :class="a.unlocked
          ? 'border-accent/30'
          : 'opacity-60 border-ink/5'"
        :style="{ animationDelay: `${i * 50}ms` }"
      >
        <div class="flex items-start gap-3">
          <div
            class="w-12 h-12 shrink-0 rounded-xl flex items-center justify-center
                   border"
            :class="a.unlocked
              ? 'bg-accent/15 border-accent/30 text-accent'
              : 'bg-ink/5 border-ink/10 text-muted'"
          >
            <AppIcon :name="a.unlocked ? (a.icon || 'check') : 'lock'" :size="22" />
          </div>
          <div class="flex-1 min-w-0">
            <h3
              class="font-semibold mb-0.5"
              :class="a.unlocked ? 'text-ink' : 'text-muted'"
            >
              {{ a.title }}
            </h3>
            <p class="text-muted text-xs leading-snug">{{ a.description }}</p>
            <p
              v-if="a.unlocked && a.unlocked_at"
              class="text-accent text-[10px] uppercase tracking-wider
                     font-semibold mt-2"
            >
              {{ new Date(a.unlocked_at).toLocaleDateString("ru-RU") }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>