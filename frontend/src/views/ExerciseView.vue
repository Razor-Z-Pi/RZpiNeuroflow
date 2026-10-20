<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import AppLayout from "@/components/AppLayout.vue";
import AppIcon from "@/components/AppIcon.vue";
import ReadingTrainer from "@/components/trainers/ReadingTrainer.vue";
import MemoryTrainer from "@/components/trainers/MemoryTrainer.vue";
import AttentionTrainer from "@/components/trainers/AttentionTrainer.vue";
import LogicTrainer from "@/components/trainers/LogicTrainer.vue";

const route = useRoute();
const router = useRouter();

const trainers = {
  reading: { title: "Скорочтение", icon: "reading", component: ReadingTrainer },
  memory: { title: "Дворец памяти", icon: "memory", component: MemoryTrainer },
  attention: { title: "Внимание", icon: "attention", component: AttentionTrainer },
  logic: { title: "Мышление", icon: "logic", component: LogicTrainer },
};

const trainer = computed(() => trainers[route.params.type]);

function goBack() {
  router.push("/");
}
</script>

<template>
  <AppLayout>
    <div v-if="!trainer" class="card text-center text-muted">
      Неизвестный тип тренировки.
    </div>

    <template v-else>
      <div class="flex items-center gap-3 mb-6">
        <button
          class="btn-ghost !py-2 !px-3 text-sm inline-flex items-center gap-2"
          @click="goBack"
        >
          <AppIcon name="back" :size="16" />
          Назад
        </button>
        <div class="flex items-center gap-2 text-muted text-sm">
          <AppIcon :name="trainer.icon" :size="16" />
          <span>{{ trainer.title }}</span>
        </div>
      </div>

      <component :is="trainer.component" :key="route.params.type" />
    </template>
  </AppLayout>
</template>