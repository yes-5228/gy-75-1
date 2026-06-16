<script setup>
defineProps({
  value: { type: String, required: true },
})
</script>

<template>
  <span class="status-badge" :data-status="value">{{ value }}</span>
</template>
