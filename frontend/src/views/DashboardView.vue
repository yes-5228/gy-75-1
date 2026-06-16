<script setup>
import { computed } from 'vue'
import DataTable from '../components/DataTable.vue'
import MetricGrid from '../components/MetricGrid.vue'
import SectionHeader from '../components/SectionHeader.vue'
import StatusBadge from '../components/StatusBadge.vue'

const props = defineProps({
  statistics: { type: Object, required: true },
  plans: { type: Array, required: true },
  faults: { type: Array, required: true },
  elevators: { type: Array, required: true },
})

const metrics = computed(() => [
  { label: 'Elevators', value: props.statistics.totalElevators || props.elevators.length, hint: 'Assets in maintenance scope' },
  { label: 'Out of Service', value: props.statistics.outOfServiceElevators || 0, hint: 'Elevators currently stopped' },
  { label: 'Open Faults', value: props.statistics.openFaults, hint: 'Pending, active, or review' },
  { label: 'Completed Repairs', value: props.statistics.completedFaults, hint: 'Closed repair tickets' },
  { label: 'Repair Cost', value: `$${props.statistics.totalCost}`, hint: 'Tracked maintenance spend' },
])

const upcomingPlans = computed(() => props.plans.slice(0, 5))
const urgentFaults = computed(() => props.faults.filter((fault) => fault.priority !== 'Normal').slice(0, 5))
</script>

<template>
  <div class="view-stack">
    <MetricGrid :metrics="metrics" />

    <div class="split-grid">
      <section class="panel">
        <SectionHeader title="Upcoming Plans" description="Sorted by scheduled date" />
        <DataTable
          :columns="[
            { key: 'title', label: 'Plan' },
            { key: 'elevatorCode', label: 'Elevator' },
            { key: 'scheduledDate', label: 'Date' },
            { key: 'status', label: 'Status' },
          ]"
          :rows="upcomingPlans"
        >
          <template #status="{ row }">
            <StatusBadge :value="row.status" />
          </template>
        </DataTable>
      </section>

      <section class="panel">
        <SectionHeader title="Priority Faults" description="High priority repair queue" />
        <DataTable
          :columns="[
            { key: 'faultType', label: 'Type' },
            { key: 'elevatorCode', label: 'Elevator' },
            { key: 'priority', label: 'Priority' },
            { key: 'status', label: 'Status' },
          ]"
          :rows="urgentFaults"
        >
          <template #priority="{ row }">
            <StatusBadge :value="row.priority" />
          </template>
          <template #status="{ row }">
            <StatusBadge :value="row.status" />
          </template>
        </DataTable>
      </section>
    </div>
  </div>
</template>
