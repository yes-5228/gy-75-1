import { get, patch, post } from './http'

export const catalogApi = {
  communities: () => get('/api/communities'),
  elevators: () => get('/api/elevators'),
}

export const maintenanceApi = {
  plans: () => get('/api/maintenance-plans'),
  createPlan: (payload) => post('/api/maintenance-plans', payload),
  updatePlan: (id, payload) => patch(`/api/maintenance-plans/${id}`, payload),
  inspections: () => get('/api/inspections'),
  createInspection: (payload) => post('/api/inspections', payload),
}

export const repairApi = {
  faults: () => get('/api/faults'),
  createFault: (payload) => post('/api/faults', payload),
  tracking: (faultId) => get(`/api/tracking${faultId ? `?faultId=${faultId}` : ''}`),
  createTracking: (payload) => post('/api/tracking', payload),
  statistics: () => get('/api/statistics'),
}
