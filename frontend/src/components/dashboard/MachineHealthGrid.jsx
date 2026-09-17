import React from 'react';
import { useNavigate } from 'react-router-dom';
import StatusBadge from '../common/StatusBadge';
import { ChevronRight } from 'lucide-react';

export default function MachineHealthGrid({ machines = [], onSelectMachine }) {
  const navigate = useNavigate();

  return (
    <div className="enterprise-card">
      <div className="p-4 border-b border-slate-200 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Machine Status & Telemetry
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Operational condition across monitored CNC equipment
          </p>
        </div>
        <button 
          onClick={() => navigate('/machines')}
          className="text-xs font-medium text-[#356B7A] hover:text-[#285664] transition-colors"
        >
          View All Machines →
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="enterprise-table">
          <thead>
            <tr>
              <th>Machine</th>
              <th>Model / Axis</th>
              <th>Status</th>
              <th>Health Index</th>
              <th>Current Tool</th>
              <th>Vibration</th>
              <th>Temperature</th>
              <th>Last Maintenance</th>
              <th>Open Issues</th>
              <th className="text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            {machines.map((m) => {
              const isCritical = m.status === 'Critical';
              const isWarning = m.status === 'Warning';

              return (
                <tr 
                  key={m.machine_id}
                  className="cursor-pointer"
                  onClick={() => onSelectMachine ? onSelectMachine(m.machine_id) : navigate('/machines')}
                >
                  <td className="font-mono font-semibold text-slate-900">{m.machine_id}</td>
                  <td className="text-slate-600">{m.model} ({m.axes}X)</td>
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
                      <span className="font-mono text-xs text-slate-700 font-medium">
                        {m.health_score}%
                      </span>
                    </div>
                  </td>
                  <td className="font-mono text-slate-700">{m.current_tool}</td>
                  <td className={`font-mono ${m.vibration > 2.0 ? 'text-[#C34B4B] font-semibold' : 'text-slate-700'}`}>
                    {m.vibration} mm/s
                  </td>
                  <td className="font-mono text-slate-700">{m.temperature} °C</td>
                  <td className="text-slate-500">{m.last_maintenance}</td>
                  <td>
                    {m.active_issues && m.active_issues.length > 0 ? (
                      <span className="text-[#C34B4B] text-xs truncate max-w-[180px] block" title={m.active_issues[0]}>
                        {m.active_issues[0]}
                      </span>
                    ) : (
                      <span className="text-slate-400 text-xs">None</span>
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
  );
}
