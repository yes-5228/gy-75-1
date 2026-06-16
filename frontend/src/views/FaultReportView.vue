﻿<script setup>
import { reactive } from 'vue'
import { Siren } from 'lucide-vue-next'
import DataTable from '../components/DataTable.vue'
import SectionHeader from '../components/SectionHeader.vue'
import StatusBadge from '../components/StatusBadge.vue'

defineProps({
  faults: { type: Array, required: true },
  elevators: { type: Array, required: true },
})

const emit = defineEmits(['create'])

const form = reactive({
  reporter: '',
  phone: '',
  faultType: 'Trapped Passenger Alarm',
  description: '',
  priority: 'Normal',
  elevatorId: '',
})

function submit() {
  emit('create', { ...form, elevatorId: Number(form.elevatorId) })
  Object.assign(form, {
    reporter: '',
    phone: '',
    faultType: 'Trapped Passenger Alarm',
    description: '',
    priority: 'Normal',
    elevatorId: '',
  })
}
</script>

<template>
  <div class="view-stack">
    <section class="panel">
      <SectionHeader title="Fault Report" description="Register source, type, priority, and description" />
      <form class="form-grid" @submit.prevent="submit">
        <label>
          <span>Reporter</span>
          <input v-model="form.reporter" required placeholder="Owner, property desk, or operator" />
        </label>
        <label>
          <span>Phone</span>
          <input v-model="form.phone" required placeholder="Mobile or landline" />
        </label>
        <label>
          <span>Fault type</span>
          <select v-model="form.faultType">
            <option>Trapped Passenger Alarm</option>
            <option>Abnormal Noise</option>
            <option>Door Failure</option>
            <option>Out of Service</option>
            <option>Other</option>
          </select>
        </label>
        <label>
          <span>Priority</span>
          <select v-model="form.priority">
            <option>Normal</option>
            <option>High</option>
            <option>Urgent</option>
          </select>
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
          <span>Description</span>
          <textarea v-model="form.description" required rows="3" placeholder="Time, floor, symptoms, and actions already taken"></textarea>
        </label>
        <button class="danger-action" type="submit">
          <Siren :size="17" />
          <span>Submit Fault</span>
        </button>
      </form>
    </section>

    <section class="panel">
      <SectionHeader title="Fault List" description="Newest reports first" />
      <DataTable
        :columns="[
          { key: 'reportedAt', label: 'Time' },
          { key: 'faultType', label: 'Type' },
          { key: 'elevatorCode', label: 'Elevator' },
          { key: 'reporter', label: 'Reporter' },
          { key: 'priority', label: 'Priority' },
          { key: 'status', label: 'Status' },
          { key: 'elevatorStatus', label: 'Elevator Status' },
          { key: 'description', label: 'Description' },
        ]"
        :rows="faults"
      >
        <template #priority="{ row }">
          <StatusBadge :value="row.priority" />
        </template>
        <template #status="{ row }">
          <StatusBadge :value="row.status" />
        </template>
        <template #elevatorStatus="{ row }">
          <StatusBadge :value="row.elevatorOutOfService ? 'Out of Service' : 'Normal'" />
        </template>
      </DataTable>
    </section>
  </div>
</template>
