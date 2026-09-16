import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

export const api = {
  // Health
  checkHealth: async () => {
    const res = await client.get('/health');
    return res.data;
  },

  // Dashboard
  getDashboardOverview: async () => {
    const res = await client.get('/api/dashboard/overview');
    return res.data;
  },

  // Machines
  getMachines: async () => {
    const res = await client.get('/api/machines');
    return res.data;
  },

  getMachineDetail: async (machineId) => {
    const res = await client.get(`/api/machines/${machineId}`);
    return res.data;
  },

  // Investigations
  getInvestigations: async () => {
    const res = await client.get('/api/investigations');
    return res.data;
  },

  getInvestigation: async (id) => {
    const res = await client.get(`/api/investigations/${id}`);
    return res.data;
  },

  analyzeFailure: async ({ componentId, machineId, failureType }) => {
    const res = await client.post('/api/investigations/analyze', {
      component_id: componentId,
      machine_id: machineId,
      failure_type: failureType,
    });
    return res.data;
  },

  // Maintenance
  getMaintenanceOverview: async () => {
    const res = await client.get('/api/maintenance');
    return res.data;
  },

  // Historical Cases
  getHistoricalCases: async (params = {}) => {
    const res = await client.get('/api/historical-cases', { params });
    return res.data;
  },

  // AI Insights
  getInsights: async () => {
    const res = await client.get('/api/insights');
    return res.data;
  },
};
