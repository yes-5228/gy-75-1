<script setup>
import { RefreshCcw } from 'lucide-vue-next'

defineProps({
  tabs: { type: Array, required: true },
  activeView: { type: String, required: true },
  title: { type: String, required: true },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

defineEmits(['switch', 'refresh'])
</script>

<template>
  <div class="app-frame">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">EM</div>
        <div>
          <h1>Elevator Care</h1>
          <p>Community maintenance console</p>
        </div>
      </div>
      <nav class="nav-list">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="nav-item"
          :class="{ active: activeView === tab.id }"
          @click="$emit('switch', tab.id)"
        >
          <component :is="tab.icon" :size="18" />
          <span>{{ tab.label }}</span>
        </button>
      </nav>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div>
          <p class="eyebrow">Residential elevator maintenance system</p>
          <h2>{{ title }}</h2>
        </div>
        <button class="icon-button" title="Refresh data" @click="$emit('refresh')">
          <RefreshCcw :size="18" />
        </button>
      </header>

      <div v-if="error" class="notice error">{{ error }}</div>
      <div v-if="loading" class="notice">Loading data...</div>
      <section class="content-area">
        <slot />
      </section>
    </main>
  </div>
</template>
