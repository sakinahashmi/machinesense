import React from 'react';
import StatusBadge from '../common/StatusBadge';

export default function ActionMatrix({ actions = [] }) {
  const immediateActions = actions.filter((a) => a.type === 'Immediate');
  const preventiveActions = actions.filter((a) => a.type === 'Preventive');

  return (
    <div className="enterprise-card">
      <div className="p-4 border-b border-slate-200 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Recommended Actions
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Prescribed immediate containment and long-term engineering actions
          </p>
        </div>
        <span className="text-xs text-slate-500">
          {actions.length} Action Items
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 divide-y lg:divide-y-0 lg:divide-x divide-slate-200">
        {/* Immediate Actions */}
        <div className="p-4 space-y-3">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-200">
            <span className="w-2 h-2 rounded-full bg-[#C34B4B]" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900">
              Immediate Actions (Containment & Tooling)
            </h4>
          </div>

          <div className="overflow-x-auto">
            <table className="enterprise-table">
              <thead>
                <tr>
                  <th className="w-16">Priority</th>
                  <th>Action</th>
                  <th>Reason</th>
                </tr>
              </thead>
              <tbody>
                {immediateActions.map((act, idx) => (
                  <tr key={idx}>
                    <td>
                      <StatusBadge status={act.priority} size="xs" />
                    </td>
                    <td className="font-medium text-slate-900">
                      {act.action}
                      <span className="block text-[11px] text-slate-500 font-mono mt-0.5">
                        Target: {act.target_component_or_tool}
                      </span>
                    </td>
                    <td className="text-xs text-slate-600">
                      {act.reason}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Preventive Actions */}
        <div className="p-4 space-y-3">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-200">
            <span className="w-2 h-2 rounded-full bg-[#356B7A]" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900">
              Preventive Actions (Process Optimization)
            </h4>
          </div>

          <div className="overflow-x-auto">
            <table className="enterprise-table">
              <thead>
                <tr>
                  <th className="w-16">Priority</th>
                  <th>Action</th>
                  <th>Reason</th>
                </tr>
              </thead>
              <tbody>
                {preventiveActions.map((act, idx) => (
                  <tr key={idx}>
                    <td>
                      <StatusBadge status={act.priority} size="xs" />
                    </td>
                    <td className="font-medium text-slate-900">
                      {act.action}
                      <span className="block text-[11px] text-slate-500 font-mono mt-0.5">
                        Target: {act.target_component_or_tool}
                      </span>
                    </td>
                    <td className="text-xs text-slate-600">
                      {act.reason}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
