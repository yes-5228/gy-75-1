<script setup>
import { reactive } from 'vue'
import { Check } from 'lucide-vue-next'
import DataTable from '../components/DataTable.vue'
import SectionHeader from '../components/SectionHeader.vue'
import StatusBadge from '../components/StatusBadge.vue'

defineProps({
  plans: { type: Array, required: true },
  elevators: { type: Array, required: true },
})

const emit = defineEmits(['create', 'update'])

const form = reactive({
  title: '',
  planType: 'Semi-monthly',
  scheduledDate: new Date().toISOString().slice(0, 10),
  assignee: '',
  elevatorId: '',
  notes: '',
})

function resetForm() {
  Object.assign(form, {
    title: '',
    planType: 'Semi-monthly',
    scheduledDate: new Date().toISOString().slice(0, 10),
    assignee: '',
    elevatorId: '',
    notes: '',
  })
}

function submit() {
  emit('create', { ...form, elevatorId: Number(form.elevatorId) })
  resetForm()
}
</script>

<template>
  <div class="view-stack">
    <section class="panel">
      <SectionHeader title="Create Maintenance Plan" description="Assign elevator, cycle, date, and engineer" />
      <form class="form-grid" @submit.prevent="submit">
        <label>
          <span>Plan name</span>
          <input v-model="form.title" required placeholder="Example: Semi-monthly inspection" />
        </label>
        <label>
          <span>Plan type</span>
          <select v-model="form.planType">
            <option>Semi-monthly</option>
            <option>Monthly</option>
            <option>Quarterly</option>
            <option>Annual test</option>
          </select>
        </label>
        <label>
          <span>Schedule date</span>
          <input v-model="form.scheduledDate" type="date" required />
        </label>
        <label>
          <span>Assignee</span>
          <input v-model="form.assignee" required placeholder="Maintenance engineer" />
        </label>
        <label>
          <span>Elevator</span>
          <select v-model="form.elevatorId" required>
            <option value="" disabled>Select elevator</option>
            <option v-for="elevator in elevators" :key="elevator.id" :value="elevator.id">
              {{ elevator.code }} - {{ elevator.communityName }}
            </option>
          </select>
        </label>
        <label class="wide">
          <span>Notes</span>
          <textarea v-model="form.notes" rows="3" placeholder="Inspection focus, spare parts, or risks"></textarea>
        </label>
        <button class="primary-action" type="submit">
          <Check :size="17" />
          <span>Save Plan</span>
        </button>
      </form>
    </section>

    <section class="panel">
      <SectionHeader title="Plan List" description="Update execution status directly" />
      <DataTable
        :columns="[
          { key: 'title', label: 'Plan' },
          { key: 'planType', label: 'Type' },
          { key: 'elevatorCode', label: 'Elevator' },
          { key: 'scheduledDate', label: 'Date' },
          { key: 'assignee', label: 'Assignee' },
          { key: 'status', label: 'Status' },
        ]"
        :rows="plans"
      >
        <template #status="{ row }">
          <select class="inline-select" :value="row.status" @change="emit('update', row.id, { status: $event.target.value })">
            <option>Pending</option>
            <option>Scheduled</option>
            <option>In Progress</option>
            <option>Completed</option>
          </select>
          <StatusBadge :value="row.status" />
        </template>
      </DataTable>
    </section>
  </div>
</template>
