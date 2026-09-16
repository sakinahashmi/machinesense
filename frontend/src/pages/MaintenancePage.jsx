import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import StatusBadge from '../components/common/StatusBadge';
import { Search } from 'lucide-react';

export default function MaintenancePage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const res = await api.getMaintenanceOverview();
        setData(res);
      } catch (err) {
        console.error('Failed to load maintenance data:', err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const alerts = data?.overdue_alerts || [];
  const toolTracker = data?.tool_wear_tracker || [];
  const history = data?.recent_history || [];

  const filteredHistory = history.filter((h) => 
    h.machine_id.toLowerCase().includes(search.toLowerCase()) ||
    h.tool_id.toLowerCase().includes(search.toLowerCase()) ||
    h.maintenance_type.toLowerCase().includes(search.toLowerCase()) ||
    h.technician_note.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="pb-2 border-b border-slate-200">
        <h1 className="text-xl font-bold text-slate-900">
          Plant Maintenance & Tool Lifecycle Management
        </h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Tool cycle accumulation, overdue tool change orders, and preventive service logs
        </p>
      </div>

      {/* Overdue Maintenance Section */}
      {alerts.length > 0 && (
        <div className="enterprise-card border-l-4 border-l-red-600">
          <div className="p-4 border-b border-slate-200">
            <h3 className="text-sm font-bold text-red-900">
              Overdue Maintenance Tickets ({alerts.length})
            </h3>
          </div>

          <div className="overflow-x-auto">
            <table className="enterprise-table">
              <thead>
                <tr>
                  <th>Ticket ID</th>
                  <th>Machine</th>
                  <th>Tool ID</th>
                  <th>Maintenance Type</th>
                  <th>Accumulated Cycles</th>
                  <th>Rated Limit</th>
                  <th>Overage</th>
                  <th>Last Replaced</th>
                  <th>Action Required</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((al) => (
                  <tr key={al.alert_id} className="bg-red-50/40">
                    <td className="font-mono font-medium text-slate-900">{al.alert_id}</td>
                    <td className="font-mono font-bold text-slate-900">{al.machine_id}</td>
                    <td className="font-mono font-bold text-amber-900">{al.tool_id}</td>
                    <td className="font-medium text-slate-900">{al.type}</td>
                    <td className="font-mono font-bold text-red-700">{al.current_cycles}</td>
                    <td className="font-mono text-slate-600">{al.max_threshold}</td>
                    <td className="font-mono font-bold text-red-700">+{al.overdue_by_cycles} cycles</td>
                    <td className="text-slate-600">{al.last_replaced}</td>
                    <td className="text-red-800 font-medium">{al.action_required}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tool Wear & Cycle Tracker */}
      <div className="enterprise-card">
        <div className="p-4 border-b border-slate-200">
          <h3 className="text-sm font-bold text-slate-900">
            Active Tool Wear Tracker
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">Machining cycles vs rated tool life threshold</p>
        </div>

        <div className="overflow-x-auto">
          <table className="enterprise-table">
            <thead>
              <tr>
                <th>Tool ID</th>
                <th>Tool Type</th>
                <th>Mounted Machine</th>
                <th>Accumulated Cycles</th>
                <th>Life Limit</th>
                <th>Wear Utilization</th>
                <th className="text-right">Condition</th>
              </tr>
            </thead>
            <tbody>
              {toolTracker.map((t) => {
                const isOver = t.cycles > t.max_cycles;
                const isNear = t.cycles >= t.max_cycles * 0.9 && !isOver;

                return (
                  <tr key={t.tool_id + t.machine_id}>
                    <td className="font-mono font-bold text-slate-900">{t.tool_id}</td>
                    <td className="text-slate-700">{t.type}</td>
                    <td className="font-mono text-slate-800">{t.machine_id}</td>
                    <td className={`font-mono ${isOver ? 'font-bold text-red-700' : 'text-slate-800'}`}>
                      {t.cycles}
                    </td>
                    <td className="font-mono text-slate-500">{t.max_cycles}</td>
                    <td>
                      <div className="flex items-center gap-2">
                        <div className="w-24 h-1.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
                          <div
                            className={`h-full ${
                              isOver ? 'bg-red-600' : isNear ? 'bg-amber-500' : 'bg-emerald-600'
                            }`}
                            style={{ width: `${Math.min(100, t.wear_pct)}%` }}
                          />
                        </div>
                        <span className={`font-mono text-xs font-semibold ${isOver ? 'text-red-700' : isNear ? 'text-amber-800' : 'text-slate-700'}`}>
                          {t.wear_pct}%
                        </span>
                      </div>
                    </td>
                    <td className="text-right">
                      <StatusBadge status={t.status} size="xs" />
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Maintenance History */}
      <div className="enterprise-card">
        <div className="p-4 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-bold text-slate-900">
              Maintenance Service History
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">Historical work orders and calibration logs</p>
          </div>

          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search maintenance logs..."
              className="bg-white border border-slate-300 rounded pl-8 pr-2.5 py-1 text-xs font-mono text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-amber-600 w-64"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="enterprise-table">
            <thead>
              <tr>
                <th>Record ID</th>
                <th>Machine</th>
                <th>Tool</th>
                <th>Service Date</th>
                <th>Maintenance Action</th>
                <th>Cycle Count</th>
                <th>Technician Notes</th>
                <th className="text-right">Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredHistory.map((h, i) => (
                <tr key={i}>
                  <td className="font-mono text-slate-700 font-medium">{h.maintenance_id}</td>
                  <td className="font-mono font-semibold text-slate-900">{h.machine_id}</td>
                  <td className="font-mono text-slate-700">{h.tool_id}</td>
                  <td className="font-mono text-slate-600 text-xs">{h.date}</td>
                  <td className="text-slate-800 font-medium">{h.maintenance_type}</td>
                  <td className="font-mono text-slate-700">{h.cycle_count}</td>
                  <td className="text-slate-600 max-w-sm truncate" title={h.technician_note}>
                    {h.technician_note}
                  </td>
                  <td className="text-right">
                    <StatusBadge status={h.status} size="xs" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
