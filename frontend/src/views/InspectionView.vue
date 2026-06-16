<script setup>
import { reactive } from 'vue'
import { Upload } from 'lucide-vue-next'
import DataTable from '../components/DataTable.vue'
import SectionHeader from '../components/SectionHeader.vue'
import StatusBadge from '../components/StatusBadge.vue'

defineProps({
  records: { type: Array, required: true },
  elevators: { type: Array, required: true },
})

const emit = defineEmits(['create'])

const form = reactive({
  inspector: '',
  result: 'Normal',
  checklist: '',
  attachmentUrl: '',
  elevatorId: '',
})

function submit() {
  emit('create', { ...form, elevatorId: Number(form.elevatorId) })
  Object.assign(form, { inspector: '', result: 'Normal', checklist: '', attachmentUrl: '', elevatorId: '' })
}
</script>

<template>
  <div class="view-stack">
    <section class="panel">
      <SectionHeader title="Upload Inspection Record" description="Register result, checklist, and attachment URL" />
      <form class="form-grid" @submit.prevent="submit">
        <label>
          <span>Inspector</span>
          <input v-model="form.inspector" required placeholder="Inspector name" />
        </label>
        <label>
          <span>Result</span>
          <select v-model="form.result">
            <option>Normal</option>
            <option>Needs Review</option>
            <option>Abnormal</option>
          </select>
        </label>
        <label>
          <span>Elevator</span>
          <select v-model="form.elevatorId" required>
            <option value="" disabled>Select elevator</option>
            <option v-for="elevator in elevators" :key="elevator.id" :value="elevator.id">
              {{ elevator.code }} - {{ elevator.building }} {{ elevator.unit }}
            </option>
          </select>
        </label>
        <label>
          <span>Attachment URL</span>
          <input v-model="form.attachmentUrl" placeholder="Image or document URL" />
        </label>
        <label class="wide">
          <span>Checklist</span>
          <textarea v-model="form.checklist" required rows="3" placeholder="Door, cabin, machine room, traction system, and safety checks"></textarea>
        </label>
        <button class="primary-action" type="submit">
          <Upload :size="17" />
          <span>Submit Record</span>
        </button>
      </form>
    </section>

    <section class="panel">
      <SectionHeader title="Inspection Ledger" description="Newest records first" />
      <DataTable
        :columns="[
          { key: 'inspectedAt', label: 'Time' },
          { key: 'elevatorCode', label: 'Elevator' },
          { key: 'inspector', label: 'Inspector' },
          { key: 'result', label: 'Result' },
          { key: 'checklist', label: 'Checklist' },
          { key: 'attachmentUrl', label: 'Attachment' },
        ]"
        :rows="records"
      >
        <template #result="{ row }">
          <StatusBadge :value="row.result" />
        </template>
        <template #attachmentUrl="{ row }">
          <a v-if="row.attachmentUrl" :href="row.attachmentUrl" target="_blank" rel="noreferrer">Open</a>
          <span v-else>-</span>
        </template>
      </DataTable>
    </section>
  </div>
</template>
