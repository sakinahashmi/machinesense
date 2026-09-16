import React from 'react';
import { useNavigate } from 'react-router-dom';
import StatusBadge from '../common/StatusBadge';
import { AlertCircle, ChevronRight } from 'lucide-react';

export default function FleetInsightAlerts({ insights = [] }) {
  const navigate = useNavigate();

  return (
    <div className="enterprise-card">
      <div className="p-4 border-b border-slate-200 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Systemic Observations & Alerts
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Cross-machine pattern correlations derived from operational logs
          </p>
        </div>
        <button
          onClick={() => navigate('/insights')}
          className="text-xs font-medium text-amber-700 hover:text-amber-800 transition-colors"
        >
          All Analysis Insights →
        </button>
      </div>

      <div className="divide-y divide-slate-100">
        {insights.map((ins) => (
          <div
            key={ins.id}
            className="p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-slate-50 transition-colors"
          >
            <div className="flex items-start gap-3">
              <div className="p-1.5 rounded bg-slate-100 text-slate-600 shrink-0 mt-0.5">
                <AlertCircle className="w-4 h-4" />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-0.5">
                  <span className="text-xs font-semibold text-slate-900">{ins.title}</span>
                  <StatusBadge status={ins.type} size="xs" />
                  <span className="text-[11px] text-slate-400 font-mono">{ins.timestamp}</span>
                </div>
                <p className="text-xs text-slate-600 leading-normal">{ins.description}</p>
              </div>
            </div>

            <button
              onClick={() => navigate('/investigations')}
              className="btn-secondary self-end sm:self-center shrink-0 text-xs py-1"
            >
              <span>{ins.action_text || 'Investigate'}</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
