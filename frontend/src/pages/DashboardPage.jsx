import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import MetricCard from '../components/common/MetricCard';
import MachineHealthGrid from '../components/dashboard/MachineHealthGrid';
import RecentInvestigationsTable from '../components/dashboard/RecentInvestigationsTable';
import FleetInsightAlerts from '../components/dashboard/FleetInsightAlerts';
import MachineTelemetryModal from '../components/machines/MachineTelemetryModal';
import { 
  Percent, 
  SearchCode, 
  AlertTriangle, 
  Cpu, 
  RefreshCw,
  TrendingUp
} from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedMachineDetail, setSelectedMachineDetail] = useState(null);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const res = await api.getDashboardOverview();
      setData(res);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const handleSelectMachine = async (machineId) => {
    try {
      const detail = await api.getMachineDetail(machineId);
      setSelectedMachineDetail(detail);
    } catch (err) {
      console.error('Failed to load machine detail:', err);
    }
  };

  const metrics = data?.metrics || {
    first_pass_yield: 94.2,
    first_pass_yield_delta: +0.4,
    active_investigations: 12,
    critical_anomalies: 3,
    machines_monitored: 8,
  };

  const passRateTrend = data?.inspection_pass_rate_trend || [];

  return (
    <div className="space-y-5">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900">
            Manufacturing Overview
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Production quality and equipment health across monitored machines.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={loadDashboard}
            className="btn-secondary py-1.5 px-2.5 text-xs"
            title="Refresh Fleet Data"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>

          <button
            onClick={() => navigate('/investigations')}
            className="btn-primary text-xs"
          >
            <SearchCode className="w-4 h-4" />
            <span>Root Cause Investigation</span>
          </button>
        </div>
      </div>

      {/* Top KPI Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        <MetricCard
          title="First Pass Yield"
          value={`${metrics.first_pass_yield}%`}
          delta={metrics.first_pass_yield_delta}
          deltaLabel="vs previous 7-day average"
          icon={Percent}
        />
        <MetricCard
          title="Active Investigations"
          value={metrics.active_investigations}
          deltaLabel="3 critical priority tickets"
          icon={SearchCode}
        />
        <MetricCard
          title="Critical Issues"
          value={metrics.critical_anomalies}
          deltaLabel="Tool wear & vibration anomalies"
          icon={AlertTriangle}
        />
        <MetricCard
          title="Machines Online"
          value={`${metrics.machines_monitored}`}
          deltaLabel="8 active machining centers"
          icon={Cpu}
        />
      </div>

      {/* Quality Trend Chart */}
      {passRateTrend.length > 0 && (
        <div className="enterprise-card p-4">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-slate-600" />
                Quality Inspection Pass Rate Trend
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">7-day rolling First Pass Yield across all production lines</p>
            </div>
            <div className="text-xs font-mono font-semibold text-slate-700 bg-slate-100 px-2 py-0.5 rounded">
              Current: {metrics.first_pass_yield}%
            </div>
          </div>

          <div className="h-44 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={passRateTrend} margin={{ top: 5, right: 20, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
                <XAxis dataKey="date" stroke="#64748B" tick={{ fontSize: 11 }} />
                <YAxis stroke="#64748B" domain={[90, 100]} tick={{ fontSize: 11 }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#CBD5E1', fontSize: '11px', borderRadius: '4px' }}
                />
                <Line type="monotone" dataKey="pass_rate" name="Pass Rate (%)" stroke="#D97706" strokeWidth={2} dot={{ r: 3, fill: '#D97706' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Machine Status Table */}
      <MachineHealthGrid 
        machines={data?.machines || []} 
        onSelectMachine={handleSelectMachine}
      />

      {/* Recent Investigations Table */}
      <RecentInvestigationsTable 
        investigations={data?.recent_investigations || []} 
      />

      {/* Systemic Observations & Alerts */}
      <FleetInsightAlerts 
        insights={data?.fleet_insights || []} 
      />

      {/* Telemetry Detail Modal */}
      {selectedMachineDetail && (
        <MachineTelemetryModal
          machine={selectedMachineDetail}
          onClose={() => setSelectedMachineDetail(null)}
        />
      )}
    </div>
  );
}
