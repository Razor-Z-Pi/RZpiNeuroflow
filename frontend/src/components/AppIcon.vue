<script setup>
defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 20 },
});
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.8"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    <!-- book-open: чтение -->
    <template v-if="name === 'reading'">
      <path d="M2 4h7a3 3 0 0 1 3 3v13a2.5 2.5 0 0 0-2.5-2.5H2z" />
      <path d="M22 4h-7a3 3 0 0 0-3 3v13a2.5 2.5 0 0 1 2.5-2.5H22z" />
    </template>

    <!-- brain: память -->
    <template v-else-if="name === 'memory'">
      <path d="M9 3a3 3 0 0 0-3 3v1a3 3 0 0 0-2 5.2A3 3 0 0 0 6 17v1a3 3 0 0 0 3 3h3V3z" />
      <path d="M15 3a3 3 0 0 1 3 3v1a3 3 0 0 1 2 5.2A3 3 0 0 1 18 17v1a3 3 0 0 1-3 3h-3V3z" />
      <path d="M12 8v8" />
    </template>

    <!-- target: внимание -->
    <template v-else-if="name === 'attention'">
      <circle cx="12" cy="12" r="9" />
      <circle cx="12" cy="12" r="5" />
      <circle cx="12" cy="12" r="1.5" fill="currentColor" />
    </template>

    <!-- puzzle: мышление -->
    <template v-else-if="name === 'logic'">
      <path d="M14 7h3a2 2 0 0 1 2 2v3a2 2 0 1 1 0 4v3a2 2 0 0 1-2 2h-3a2 2 0 1 1-4 0H7a2 2 0 0 1-2-2v-3a2 2 0 1 1 0-4V9a2 2 0 0 1 2-2h3a2 2 0 1 1 4 0z" />
    </template>

    <!-- chart: статистика -->
    <template v-else-if="name === 'chart'">
      <path d="M3 3v18h18" />
      <path d="M7 14l4-4 4 3 5-6" />
    </template>

    <!-- logout -->
    <template v-else-if="name === 'logout'">
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
      <path d="M16 17l5-5-5-5" />
      <path d="M21 12H9" />
    </template>

    <!-- flame: стрик -->
    <template v-else-if="name === 'flame'">
      <path d="M12 2s4 4 4 8a4 4 0 1 1-8 0c0-1.5.5-2.5.5-2.5S6 9 6 13a6 6 0 1 0 12 0c0-6-6-11-6-11z" />
    </template>

    <!-- arrow-left -->
    <template v-else-if="name === 'back'">
      <path d="M19 12H5" />
      <path d="M12 19l-7-7 7-7" />
    </template>

    <!-- check -->
    <template v-else-if="name === 'check'">
      <path d="M20 6L9 17l-5-5" />
    </template>

    <!-- arrow-up -->
    <template v-else-if="name === 'trend-up'">
      <path d="M22 7l-8.5 8.5-5-5L2 17" />
      <path d="M16 7h6v6" />
    </template>

    <!-- sun -->
    <template v-else-if="name === 'sun'">
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />
    </template>

    <!-- moon -->
    <template v-else-if="name === 'moon'">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </template>

    <!-- settings -->
    <template v-else-if="name === 'settings'">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
    </template>

    <template v-else-if="name === 'trophy'">
      <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" />
      <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" />
      <path d="M4 22h16" />
      <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22" />
      <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22" />
      <path d="M18 2H6v7a6 6 0 0 0 12 0V2z" />
    </template>

    <!-- lock -->
    <template v-else-if="name === 'lock'">
      <rect x="3" y="11" width="18" height="11" rx="2" />
      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
    </template>
  </svg>
</template>