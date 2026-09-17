import React from 'react';
import StatusBadge from '../common/StatusBadge';
import { X, AlertTriangle } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine } from 'recharts';

export default function MachineTelemetryModal({ machine, onClose }) {
  if (!machine) return null;

  const telemetry = machine.recent_telemetry || [];

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-[2px] flex items-center justify-center p-4">
      <div className="bg-white border border-slate-300 rounded-md max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-xl">
        {/* Header */}
        <div className="p-4 border-b border-slate-200 flex items-center justify-between sticky top-0 bg-white z-10">
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-bold text-slate-900 font-mono">{machine.machine_id}</h3>
              <StatusBadge status={machine.status} size="xs" />
            </div>
            <p className="text-xs text-slate-500 font-mono mt-0.5">{machine.model} · {machine.axes}-Axis Machining Center</p>
          </div>

          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-slate-100 text-slate-500 hover:text-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 space-y-5">
          {/* Active Alerts */}
          {machine.active_alerts && machine.active_alerts.length > 0 && (
            <div className="p-3 rounded bg-[#F9EBEB] border border-[#F2CDCD] space-y-1">
              <div className="flex items-center gap-1.5 text-xs font-bold text-[#C34B4B] uppercase">
                <AlertTriangle className="w-4 h-4 text-[#C34B4B]" />
                Active Alerts
              </div>
              {machine.active_alerts.map((al, idx) => (
                <p key={idx} className="text-xs text-[#C34B4B] font-mono pl-5">
                  • {al}
                </p>
              ))}
            </div>
          )}

          {/* Metrics Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="p-3 rounded bg-slate-50 border border-slate-200">
              <span className="text-slate-500 block text-[11px] uppercase">Vibration RMS</span>
              <span className={`text-base font-mono font-bold ${machine.latest_telemetry?.vibration > 2.0 ? 'text-[#C34B4B]' : 'text-slate-900'}`}>
                {machine.latest_telemetry?.vibration || machine.nominal_vib} mm/s
              </span>
            </div>
            <div className="p-3 rounded bg-slate-50 border border-slate-200">
              <span className="text-slate-500 block text-[11px] uppercase">Cutting Power</span>
              <span className="text-base font-mono font-bold text-slate-900">
                {machine.latest_telemetry?.power_consumption || machine.nominal_power} kW
              </span>
            </div>
            <div className="p-3 rounded bg-slate-50 border border-slate-200">
              <span className="text-slate-500 block text-[11px] uppercase">Temperature</span>
              <span className="text-base font-mono font-bold text-slate-900">
                {machine.latest_telemetry?.temperature || machine.nominal_temp} °C
              </span>
            </div>
            <div className="p-3 rounded bg-slate-50 border border-slate-200">
              <span className="text-slate-500 block text-[11px] uppercase">Current Tool</span>
              <span className="text-base font-mono font-bold text-[#356B7A]">
                {machine.current_tool}
              </span>
            </div>
          </div>

          {/* Telemetry Stream Chart */}
          <div>
            <h4 className="text-xs font-bold uppercase text-slate-700 tracking-wider mb-2">
              Recent Spindle Vibration Telemetry (mm/s)
            </h4>
            <div className="h-44 w-full bg-white p-2 rounded border border-slate-200">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={telemetry.slice(-25)}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#D8E0E6" vertical={false} />
                  <XAxis dataKey="timestamp" stroke="#667685" tick={{ fontSize: 9 }} tickFormatter={(t) => t.slice(11, 16)} />
                  <YAxis stroke="#667685" tick={{ fontSize: 9 }} domain={[0, 4.5]} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#D8E0E6', fontSize: '11px', fontFamily: 'monospace' }}
                  />
                  <ReferenceLine y={2.0} stroke="#C34B4B" strokeDasharray="3 3" label={{ value: '2.0 mm/s limit', fill: '#C34B4B', fontSize: 9 }} />
                  <Line type="monotone" dataKey="vibration" stroke="#5C6F7E" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Recent Maintenance & Inspections */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="p-3 rounded bg-slate-50 border border-slate-200">
              <span className="text-slate-700 font-bold block mb-2 uppercase text-[11px]">
                Recent Maintenance Events
              </span>
              <div className="space-y-2 font-mono">
                {machine.recent_maintenance?.slice(0, 3).map((m, i) => (
                  <div key={i} className="text-slate-700 pb-1.5 border-b border-slate-200 last:border-0">
                    <span className="font-semibold text-slate-900">{m.maintenance_type}</span> ({m.date})
                    <p className="text-[11px] text-slate-500 truncate">{m.technician_note}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="p-3 rounded bg-slate-50 border border-slate-200">
              <span className="text-slate-700 font-bold block mb-2 uppercase text-[11px]">
                Recent Quality Inspections
              </span>
              <div className="space-y-2 font-mono">
                {machine.recent_inspections?.slice(0, 3).map((insp, i) => (
                  <div key={i} className="text-slate-700 pb-1.5 border-b border-slate-200 last:border-0 flex justify-between">
                    <div>
                      <span className="font-semibold text-slate-900">{insp.component_id}</span>
                      <p className="text-[11px] text-slate-500">Dev: +{insp.deviation} mm</p>
                    </div>
                    <StatusBadge status={insp.result} size="xs" />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
