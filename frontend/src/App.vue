<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { Activity, ClipboardCheck, FileClock, LayoutDashboard, Wrench } from 'lucide-vue-next'
import { catalogApi, maintenanceApi, repairApi } from './api/modules'
import AppShell from './components/AppShell.vue'
import DashboardView from './views/DashboardView.vue'
import FaultReportView from './views/FaultReportView.vue'
import InspectionView from './views/InspectionView.vue'
import MaintenancePlanView from './views/MaintenancePlanView.vue'
import RepairTrackingView from './views/RepairTrackingView.vue'

const activeView = ref('dashboard')
const loading = ref(false)
const error = ref('')

const state = reactive({
  communities: [],
  elevators: [],
  plans: [],
  inspections: [],
  faults: [],
  tracking: [],
  statistics: {
    totalFaults: 0,
    openFaults: 0,
    completedFaults: 0,
    totalCost: 0,
    statusCounts: {},
    priorityCounts: {},
  },
})

const tabs = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'plans', label: 'Maintenance Plans', icon: FileClock },
  { id: 'inspections', label: 'Inspections', icon: ClipboardCheck },
  { id: 'faults', label: 'Fault Reports', icon: Activity },
  { id: 'tracking', label: 'Repair Tracking', icon: Wrench },
]

const currentTitle = computed(() => tabs.find((tab) => tab.id === activeView.value)?.label || '')

async function loadAll() {
  loading.value = true
  error.value = ''
  try {
    const [communities, elevators, plans, inspections, faults, tracking, statistics] = await Promise.all([
      catalogApi.communities(),
      catalogApi.elevators(),
      maintenanceApi.plans(),
      maintenanceApi.inspections(),
      repairApi.faults(),
      repairApi.tracking(),
      repairApi.statistics(),
    ])
    state.communities = communities.items
    state.elevators = elevators.items
    state.plans = plans.items
    state.inspections = inspections.items
    state.faults = faults.items
    state.tracking = tracking.items
    state.statistics = statistics
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function createPlan(payload) {
  await maintenanceApi.createPlan(payload)
  await loadAll()
}

async function updatePlan(id, payload) {
  await maintenanceApi.updatePlan(id, payload)
  await loadAll()
}

async function createInspection(payload) {
  await maintenanceApi.createInspection(payload)
  await loadAll()
}

async function createFault(payload) {
  await repairApi.createFault(payload)
  await loadAll()
}

async function createTracking(payload) {
  await repairApi.createTracking(payload)
  await loadAll()
}

onMounted(loadAll)
</script>

<template>
  <AppShell
    :tabs="tabs"
    :active-view="activeView"
    :title="currentTitle"
    :loading="loading"
    :error="error"
    @switch="activeView = $event"
    @refresh="loadAll"
  >
    <DashboardView
      v-if="activeView === 'dashboard'"
      :statistics="state.statistics"
      :plans="state.plans"
      :faults="state.faults"
      :elevators="state.elevators"
    />
    <MaintenancePlanView
      v-else-if="activeView === 'plans'"
      :plans="state.plans"
      :elevators="state.elevators"
      @create="createPlan"
      @update="updatePlan"
    />
    <InspectionView
      v-else-if="activeView === 'inspections'"
      :records="state.inspections"
      :elevators="state.elevators"
      @create="createInspection"
    />
    <FaultReportView
      v-else-if="activeView === 'faults'"
      :faults="state.faults"
      :elevators="state.elevators"
      @create="createFault"
    />
    <RepairTrackingView
      v-else
      :faults="state.faults"
      :logs="state.tracking"
      @create="createTracking"
    />
  </AppShell>
</template>
