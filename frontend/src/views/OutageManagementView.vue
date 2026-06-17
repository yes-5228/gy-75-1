<script setup>
import { reactive, ref, computed } from 'vue'
import { Power, RotateCcw } from 'lucide-vue-next'
import DataTable from '../components/DataTable.vue'
import SectionHeader from '../components/SectionHeader.vue'
import StatusBadge from '../components/StatusBadge.vue'

const props = defineProps({
  records: { type: Array, required: true },
  elevators: { type: Array, required: true },
})

const emit = defineEmits(['register', 'restore'])

const form = reactive({
  reason: '',
  reasonType: 'Fault',
  startTime: '',
  expectedRecoveryTime: '',
  operator: '',
  notes: '',
  elevatorId: '',
})

const restoreModal = ref(false)
const restoreTargetId = ref(null)
const restoreNotes = ref('')
const restoreTargetRecord = ref(null)

const outOfServiceElevators = computed(() =>
  props.elevators.filter((e) => e.isOutOfService)
)

function resetForm() {
  Object.assign(form, {
    reason: '',
    reasonType: 'Fault',
    startTime: '',
    expectedRecoveryTime: '',
    operator: '',
    notes: '',
    elevatorId: '',
  })
}

function submit() {
  const payload = {
    ...form,
    elevatorId: Number(form.elevatorId),
  }
  if (!payload.startTime) {
    delete payload.startTime
  }
  if (!payload.expectedRecoveryTime) {
    delete payload.expectedRecoveryTime
  }
  emit('register', payload)
  resetForm()
}

function openRestoreModal(recordId) {
  const record = props.records.find((r) => r.id === recordId)
  restoreTargetId.value = recordId
  restoreTargetRecord.value = record || null
  restoreNotes.value = ''
  restoreModal.value = true
}

function cancelRestore() {
  restoreModal.value = false
  restoreTargetId.value = null
  restoreTargetRecord.value = null
  restoreNotes.value = ''
}

function confirmRestore() {
  if (!restoreNotes.value.trim()) return
  emit('restore', restoreTargetId.value, { notes: restoreNotes.value.trim() })
  restoreModal.value = false
  restoreTargetId.value = null
  restoreTargetRecord.value = null
  restoreNotes.value = ''
}

function getStatusLabel(record) {
  return record.isActive ? 'Out of Service' : 'Restored'
}
</script>

<template>
  <div class="view-stack">
    <section class="panel">
      <SectionHeader title="Register Outage" description="Record outage reason, timeline, and operator" />
      <form class="form-grid" @submit.prevent="submit">
        <label>
          <span>Elevator</span>
          <select v-model="form.elevatorId" required>
            <option value="" disabled>Select elevator</option>
            <option v-for="elevator in elevators" :key="elevator.id" :value="elevator.id">
              {{ elevator.code }} - {{ elevator.communityName }}{{ elevator.isOutOfService ? ' (Out of Service)' : '' }}
            </option>
          </select>
        </label>
        <label>
          <span>Reason type</span>
          <select v-model="form.reasonType">
            <option value="Fault">Fault</option>
            <option value="Maintenance">Maintenance</option>
            <option value="Inspection">Inspection</option>
            <option value="Other">Other</option>
          </select>
        </label>
        <label>
          <span>Operator</span>
          <input v-model="form.operator" required placeholder="Operator name" />
        </label>
        <label>
          <span>Start time</span>
          <input v-model="form.startTime" type="datetime-local" />
        </label>
        <label>
          <span>Expected recovery</span>
          <input v-model="form.expectedRecoveryTime" type="datetime-local" />
        </label>
        <label class="wide">
          <span>Reason</span>
          <input v-model="form.reason" required placeholder="Brief description of the outage reason" />
        </label>
        <label class="wide">
          <span>Notes</span>
          <textarea v-model="form.notes" rows="2" placeholder="Additional details or context"></textarea>
        </label>
        <button class="danger-action" type="submit">
          <Power :size="17" />
          <span>Register Outage</span>
        </button>
      </form>
    </section>

    <section class="panel">
      <SectionHeader title="Currently Out of Service" description="Active outage records" />
      <div v-if="outOfServiceElevators.length === 0" class="empty">No elevators currently out of service</div>
      <DataTable
        v-else
        :columns="[
          { key: 'elevatorCode', label: 'Elevator' },
          { key: 'communityName', label: 'Community' },
          { key: 'reason', label: 'Reason' },
          { key: 'startTime', label: 'Start time' },
          { key: 'expectedRecoveryTime', label: 'Expected recovery' },
          { key: 'operator', label: 'Operator' },
          { key: 'action', label: 'Action' },
        ]"
        :rows="records.filter((r) => r.isActive)"
      >
        <template #action="{ row }">
          <button class="primary-action restore-btn" @click="openRestoreModal(row.id)">
            <RotateCcw :size="14" />
            <span>Restore</span>
          </button>
        </template>
      </DataTable>
    </section>

    <section class="panel">
      <SectionHeader title="Outage History" description="All outage records" />
      <DataTable
        :columns="[
          { key: 'elevatorCode', label: 'Elevator' },
          { key: 'communityName', label: 'Community' },
          { key: 'reasonType', label: 'Type' },
          { key: 'reason', label: 'Reason' },
          { key: 'startTime', label: 'Start' },
          { key: 'endTime', label: 'End' },
          { key: 'operator', label: 'Operator' },
          { key: 'status', label: 'Status' },
        ]"
        :rows="records"
      >
        <template #status="{ row }">
          <StatusBadge :value="getStatusLabel(row)" />
        </template>
      </DataTable>
    </section>

    <div v-if="restoreModal" class="modal-overlay" @click.self="cancelRestore">
      <div class="modal-box">
        <h3>Restore Elevator Service</h3>
        <div v-if="restoreTargetRecord" class="modal-record-info">
          <div class="info-row">
            <span class="info-label">Elevator:</span>
            <span class="info-value">{{ restoreTargetRecord.elevatorCode }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Community:</span>
            <span class="info-value">{{ restoreTargetRecord.communityName }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Outage reason:</span>
            <span class="info-value">{{ restoreTargetRecord.reason }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Reason type:</span>
            <span class="info-value">{{ restoreTargetRecord.reasonType }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">Start time:</span>
            <span class="info-value">{{ restoreTargetRecord.startTime }}</span>
          </div>
        </div>
        <p class="modal-hint">Please provide a recovery description before restoring service.</p>
        <label>
          <span>Recovery notes</span>
          <textarea v-model="restoreNotes" rows="3" required placeholder="Describe what was done, parts replaced, tests performed, etc."></textarea>
        </label>
        <div class="modal-actions">
          <button class="btn-cancel" @click="cancelRestore">Cancel</button>
          <button class="primary-action" :disabled="!restoreNotes.trim()" @click="confirmRestore">
            <RotateCcw :size="14" />
            <span>Confirm Restore</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
