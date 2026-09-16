import React, { useState } from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceLine,
} from 'recharts';

export default function TrendCharts({ trends = [] }) {
  const [activeTab, setActiveTab] = useState('deviation');

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white border border-slate-300 p-2.5 rounded shadow text-xs font-mono text-slate-800">
          <p className="font-bold text-slate-900 mb-1">Time: {data.timestamp} {data.component_id ? `(${data.component_id})` : ''}</p>
          {data.dimensional_deviation !== null && (
            <p className="text-red-700 font-semibold">Deviation: +{data.dimensional_deviation} mm</p>
          )}
          <p className="text-slate-700">Vibration: {data.vibration} mm/s</p>
          <p className="text-slate-700">Power: {data.power_consumption} kW</p>
          <p className="text-slate-700">Temperature: {data.temperature} °C</p>
          {data.cycle_count && <p className="text-slate-500">Tool Cycles: {data.cycle_count}</p>}
          {data.is_failure_point && (
            <p className="mt-1 text-red-700 font-bold border-t border-slate-200 pt-1">★ Non-Conformance Point (CNC-2847)</p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="enterprise-card p-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3 pb-3 border-b border-slate-200">
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Correlated Telemetry & Dimensional Drift
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Pre-failure telemetry trends across 35 consecutive machining cycles
          </p>
        </div>

        {/* Chart Selector Tabs */}
        <div className="flex items-center gap-1 bg-slate-100 p-0.5 rounded border border-slate-200 self-start">
          <button
            onClick={() => setActiveTab('deviation')}
            className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
              activeTab === 'deviation'
                ? 'bg-white text-slate-900 font-semibold shadow-sm border border-slate-200'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Dimensional Drift
          </button>
          <button
            onClick={() => setActiveTab('vibration')}
            className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
              activeTab === 'vibration'
                ? 'bg-white text-slate-900 font-semibold shadow-sm border border-slate-200'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Spindle Vibration
          </button>
          <button
            onClick={() => setActiveTab('power')}
            className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
              activeTab === 'power'
                ? 'bg-white text-slate-900 font-semibold shadow-sm border border-slate-200'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Cutting Power
          </button>
          <button
            onClick={() => setActiveTab('temperature')}
            className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
              activeTab === 'temperature'
                ? 'bg-white text-slate-900 font-semibold shadow-sm border border-slate-200'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Temperature
          </button>
        </div>
      </div>

      {/* Recharts Canvas */}
      <div className="h-60 w-full">
        <ResponsiveContainer width="100%" height="100%">
          {activeTab === 'deviation' ? (
            <LineChart data={trends} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
              <XAxis dataKey="timestamp" stroke="#64748B" tick={{ fontSize: 10, fontFamily: 'monospace' }} />
              <YAxis stroke="#64748B" tick={{ fontSize: 10, fontFamily: 'monospace' }} domain={[0, 0.5]} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0.10} stroke="#DC2626" strokeDasharray="3 3" label={{ value: 'Upper Tol Limit (+0.10 mm)', fill: '#DC2626', fontSize: 10, position: 'top' }} />
              <Line
                type="monotone"
                dataKey="dimensional_deviation"
                name="Deviation (mm)"
                stroke="#D97706"
                strokeWidth={2}
                dot={(props) => {
                  const isFail = props.payload.is_failure_point;
                  return isFail ? (
                    <circle cx={props.cx} cy={props.cy} r={5} fill="#DC2626" stroke="#FFFFFF" strokeWidth={2} key={props.key} />
                  ) : (
                    <circle cx={props.cx} cy={props.cy} r={2} fill="#D97706" key={props.key} />
                  );
                }}
              />
            </LineChart>
          ) : activeTab === 'vibration' ? (
            <LineChart data={trends} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
              <XAxis dataKey="timestamp" stroke="#64748B" tick={{ fontSize: 10, fontFamily: 'monospace' }} />
              <YAxis stroke="#64748B" tick={{ fontSize: 10, fontFamily: 'monospace' }} domain={[0, 4.5]} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={2.0} stroke="#DC2626" strokeDasharray="3 3" label={{ value: 'Vibration Limit (2.0 mm/s)', fill: '#DC2626', fontSize: 10 }} />
              <Line type="monotone" dataKey="vibration" stroke="#2563EB" strokeWidth={2} dot={false} />
            </LineChart>
          ) : activeTab === 'power' ? (
            <LineChart data={trends} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
              <XAxis dataKey="timestamp" stroke="#64748B" tick={{ fontSize: 10, fontFamily: 'monospace' }} />
              <YAxis stroke="#64748B" tick={{ fontSize: 10, fontFamily: 'monospace' }} domain={[3.5, 5.8]} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={4.6} stroke="#DC2626" strokeDasharray="3 3" label={{ value: 'Nominal Baseline Limit (4.60 kW)', fill: '#DC2626', fontSize: 10 }} />
              <Line type="monotone" dataKey="power_consumption" stroke="#D97706" strokeWidth={2} dot={false} />
            </LineChart>
          ) : (
            <LineChart data={trends} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
              <XAxis dataKey="timestamp" stroke="#64748B" tick={{ fontSize: 10, fontFamily: 'monospace' }} />
              <YAxis stroke="#64748B" tick={{ fontSize: 10, fontFamily: 'monospace' }} domain={[30, 50]} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={42.0} stroke="#DC2626" strokeDasharray="3 3" label={{ value: 'Thermal Warning (42°C)', fill: '#DC2626', fontSize: 10 }} />
              <Line type="monotone" dataKey="temperature" stroke="#16A34A" strokeWidth={2} dot={false} />
            </LineChart>
          )}
        </ResponsiveContainer>
      </div>

      <div className="mt-2.5 pt-2 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500 font-mono">
        <span>Sampling Rate: 100% component inspection log stream</span>
        <span className="text-slate-700 font-semibold">
          {activeTab === 'deviation' ? 'Status: Progressive dimensional drift (+0.012 mm/part)' : activeTab === 'vibration' ? 'Status: Harmonic vibration chattering detected' : 'Status: Motor cutting power overload (+26.4%)'}
        </span>
      </div>
    </div>
  );
}
