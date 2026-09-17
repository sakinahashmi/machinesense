import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function MetricCard({ title, value, unit = '', delta, deltaLabel, icon: Icon, statusColor }) {
  const isPositive = typeof delta === 'number' ? delta >= 0 : false;

  return (
    <div className="enterprise-card p-4">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-xs font-medium text-slate-500 uppercase tracking-wide block">
            {title}
          </span>
          <div className="mt-1.5 flex items-baseline gap-1.5">
            <span className="text-2xl font-bold tracking-tight text-slate-900 font-mono">
              {value}
            </span>
            {unit && <span className="text-xs font-medium text-slate-500">{unit}</span>}
          </div>
        </div>

        {Icon && (
          <div className="p-2 rounded bg-slate-50 border border-slate-200 text-slate-600">
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

        {(delta !== undefined || deltaLabel) && (
        <div className="mt-2.5 pt-2 border-t border-slate-200 flex items-center gap-1.5 text-xs">
          {delta !== undefined && (
            <span className={`inline-flex items-center font-medium font-mono ${isPositive ? 'text-[#23805A]' : 'text-[#C34B4B]'}`}>
              {isPositive ? <TrendingUp className="w-3 h-3 mr-0.5" /> : <TrendingDown className="w-3 h-3 mr-0.5" />}
              {isPositive ? `+${delta}%` : `${delta}%`}
            </span>
          )}
          {deltaLabel && <span className="text-slate-500">{deltaLabel}</span>}
        </div>
      )}
    </div>
  );
}
