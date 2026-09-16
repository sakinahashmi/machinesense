import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import StatusBadge from '../components/common/StatusBadge';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Cell } from 'recharts';

export default function AIInsightsPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const res = await api.getInsights();
        setData(res);
      } catch (err) {
        console.error('Failed to load insights:', err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const patterns = data?.fleet_patterns || [];
  const distribution = data?.anomaly_distribution || [];

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="pb-2 border-b border-slate-200">
        <h1 className="text-xl font-bold text-slate-900">
          Analysis Insights
        </h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Data-derived observations and systemic failure signatures across monitored machinery
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left: Observations */}
        <div className="lg:col-span-7 space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
            Systemic Failure Patterns ({patterns.length} Identified)
          </h3>

          {patterns.map((pat) => (
            <div
              key={pat.id}
              className="enterprise-card p-4 space-y-2.5 border-l-4 border-l-amber-600"
            >
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs font-bold text-slate-800 uppercase">
                  {pat.category}
                </span>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-semibold text-slate-700">{pat.confidence}% Confidence</span>
                  <StatusBadge status={pat.severity} size="xs" />
                </div>
              </div>

              <h4 className="text-sm font-bold text-slate-900">
                {pat.title}
              </h4>

              <p className="text-xs text-slate-600 leading-relaxed">
                {pat.insight}
              </p>

              <div className="p-2.5 rounded bg-slate-50 border border-slate-200 text-xs text-slate-800">
                <span className="text-slate-500 block text-[11px] uppercase font-bold">Recommended Engineering Action:</span>
                <span className="font-medium">{pat.recommended_action}</span>
              </div>

              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500 font-mono">
                <span>Impacted Machines: <strong className="text-slate-700">{pat.impacted_machines?.join(', ')}</strong></span>
                <span>Tools: <strong className="text-slate-700">{pat.impacted_tools?.join(', ')}</strong></span>
              </div>
            </div>
          ))}
        </div>

        {/* Right: Anomaly Distribution */}
        <div className="lg:col-span-5 space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
            Root Cause Distribution
          </h3>

          <div className="enterprise-card p-4">
            <p className="text-xs text-slate-500 mb-3 font-mono">
              Frequency across 60+ historical incidents
            </p>

            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={distribution} layout="vertical" margin={{ top: 5, right: 20, left: 30, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" horizontal={false} />
                  <XAxis type="number" stroke="#64748B" tick={{ fontSize: 10, fontFamily: 'monospace' }} unit="%" />
                  <YAxis dataKey="name" type="category" stroke="#64748B" tick={{ fontSize: 10 }} width={80} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#CBD5E1', fontSize: '11px', fontFamily: 'monospace' }}
                  />
                  <Bar dataKey="percentage" fill="#D97706" radius={[0, 2, 2, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-3 pt-2.5 border-t border-slate-200 space-y-1.5 text-xs">
              {distribution.map((d) => (
                <div key={d.name} className="flex items-center justify-between font-mono">
                  <span className="text-slate-600">{d.name}</span>
                  <span className="font-semibold text-slate-900">{d.count} cases ({d.percentage}%)</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
