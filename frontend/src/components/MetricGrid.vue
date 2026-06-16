<script setup>
defineProps({
  metrics: { type: Array, required: true },
})
</script>

<template>
  <div class="metric-grid">
    <article v-for="metric in metrics" :key="metric.label" class="metric-card">
      <p>{{ metric.label }}</p>
      <strong>{{ metric.value }}</strong>
      <span>{{ metric.hint }}</span>
    </article>
  </div>
</template>
