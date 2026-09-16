import React from 'react';
import StatusBadge from '../common/StatusBadge';

export default function EvidencePanel({ rootCause }) {
  if (!rootCause) return null;

  return (
    <div className="enterprise-card p-4">
      <div className="flex items-center justify-between mb-3 pb-3 border-b border-slate-200">
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Evidence: {rootCause.root_cause}
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Signals supporting the root-cause assessment
          </p>
        </div>
        <span className="text-xs font-mono font-medium text-slate-600 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
          {rootCause.evidence?.length || 0} Correlated Signals
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {rootCause.evidence?.map((item, idx) => (
          <div
            key={idx}
            className="p-3 bg-slate-50 border border-slate-200 rounded text-xs space-y-2"
          >
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-900 uppercase text-[11px] tracking-wide">
                {item.category}: {item.title}
              </span>
              <StatusBadge status={item.badge} size="xs" />
            </div>

            <p className="text-slate-700 leading-relaxed">
              {item.description}
            </p>

            {item.metrics && Object.keys(item.metrics).length > 0 && (
              <div className="pt-2 border-t border-slate-200 flex flex-wrap gap-2 text-[11px] font-mono">
                {Object.entries(item.metrics).map(([k, v]) => (
                  <span
                    key={k}
                    className="bg-white px-1.5 py-0.5 rounded border border-slate-300 text-slate-700"
                  >
                    {k.replace(/_/g, ' ')}: <strong className="text-slate-900">{String(v)}</strong>
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {rootCause.affected_parameters && rootCause.affected_parameters.length > 0 && (
        <div className="mt-3 pt-2.5 border-t border-slate-200 flex items-center justify-between text-xs">
          <span className="text-slate-500 font-medium">Affected Parameters:</span>
          <div className="flex flex-wrap gap-1.5 font-mono">
            {rootCause.affected_parameters.map((p, i) => (
              <span key={i} className="text-slate-700 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                {p}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
