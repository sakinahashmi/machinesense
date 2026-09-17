import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import StatusBadge from '../components/common/StatusBadge';
import MachineTelemetryModal from '../components/machines/MachineTelemetryModal';
import { Search, ChevronRight } from 'lucide-react';

export default function MachinesPage() {
  const [machines, setMachines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('ALL');
  const [search, setSearch] = useState('');
  const [selectedMachine, setSelectedMachine] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const res = await api.getMachines();
        setMachines(res);
      } catch (err) {
        console.error('Failed to load machines:', err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const handleOpenDetail = async (machineId) => {
    try {
      const detail = await api.getMachineDetail(machineId);
      setSelectedMachine(detail);
    } catch (err) {
      console.error('Failed to load machine detail:', err);
    }
  };

  const filtered = machines.filter((m) => {
    const matchStatus = filterStatus === 'ALL' || m.status.toUpperCase() === filterStatus;
    const matchSearch = m.machine_id.toLowerCase().includes(search.toLowerCase()) ||
      m.model.toLowerCase().includes(search.toLowerCase()) ||
      m.current_tool.toLowerCase().includes(search.toLowerCase());
    return matchStatus && matchSearch;
  });

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900">
            Equipment Fleet Monitor
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Operational status and live telemetry across all CNC machining centers
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex items-center gap-2.5 flex-wrap">
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search machine, model..."
              className="bg-white border border-slate-300 rounded pl-8 pr-2.5 py-1 text-xs font-mono text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-[#356B7A]"
            />
          </div>

          <div className="flex items-center bg-slate-100 p-0.5 rounded border border-slate-200 text-xs">
            {['ALL', 'CRITICAL', 'WARNING', 'NOMINAL'].map((st) => (
              <button
                key={st}
                onClick={() => setFilterStatus(st)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                  filterStatus === st
                    ? 'bg-white text-slate-900 font-semibold shadow-sm border border-slate-200'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {st}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Machine Table */}
      <div className="enterprise-card">
        <div className="p-4 border-b border-slate-200">
          <h3 className="text-sm font-bold text-slate-900">
            Machining Centers ({filtered.length} Machines)
          </h3>
        </div>

        <div className="overflow-x-auto">
          <table className="enterprise-table">
            <thead>
              <tr>
                <th>Machine ID</th>
                <th>Model</th>
                <th>Axes</th>
                <th>Status</th>
                <th>Health Score</th>
                <th>Current Tool</th>
                <th>Vibration</th>
                <th>Power</th>
                <th>Temperature</th>
                <th>Last Service</th>
                <th>Active Issues</th>
                <th className="text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((m) => {
                const isCritical = m.status === 'Critical';
                const isWarning = m.status === 'Warning';

                return (
                  <tr
                    key={m.machine_id}
                    className="cursor-pointer"
                    onClick={() => handleOpenDetail(m.machine_id)}
                  >
                    <td className="font-mono font-bold text-slate-900">{m.machine_id}</td>
                    <td className="text-slate-700">{m.model}</td>
                    <td className="font-mono text-slate-600">{m.axes}-Axis</td>
                    <td>
                      <StatusBadge status={m.status} size="xs" />
                    </td>
                    <td>
                      <div className="flex items-center gap-2">
                        <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
                          <div
                            className={`h-full ${
                              isCritical ? 'bg-[#C34B4B]' : isWarning ? 'bg-[#C58A20]' : 'bg-[#23805A]'
                            }`}
                            style={{ width: `${m.health_score}%` }}
                          />
                        </div>
                        <span className="font-mono text-xs font-semibold text-slate-900">
                          {m.health_score}%
                        </span>
                      </div>
                    </td>
                    <td className="font-mono font-medium text-slate-800">{m.current_tool}</td>
                    <td className={`font-mono ${m.vibration > 2.0 ? 'text-[#C34B4B] font-semibold' : 'text-slate-700'}`}>
                      {m.vibration} mm/s
                    </td>
                    <td className="font-mono text-slate-700">{m.power_consumption} kW</td>
                    <td className="font-mono text-slate-700">{m.temperature} °C</td>
                    <td className="text-slate-500">{m.last_maintenance}</td>
                    <td>
                      {m.active_issues && m.active_issues.length > 0 ? (
                        <span className="text-[#C34B4B] text-xs truncate max-w-[160px] block" title={m.active_issues[0]}>
                          {m.active_issues[0]}
                        </span>
                      ) : (
                        <span className="text-slate-400 text-xs">Nominal</span>
                      )}
                    </td>
                    <td className="text-right">
                      <button className="text-slate-400 hover:text-slate-700 p-1">
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Telemetry Detail Modal */}
      {selectedMachine && (
        <MachineTelemetryModal
          machine={selectedMachine}
          onClose={() => setSelectedMachine(null)}
        />
      )}
    </div>
  );
}
