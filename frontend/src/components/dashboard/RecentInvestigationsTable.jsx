import React from 'react';
import { useNavigate } from 'react-router-dom';
import StatusBadge from '../common/StatusBadge';
import { ChevronRight } from 'lucide-react';

export default function RecentInvestigationsTable({ investigations = [] }) {
  const navigate = useNavigate();

  return (
    <div className="enterprise-card">
      <div className="p-4 border-b border-slate-200 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Recent Quality Investigations
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Log of dimensional and surface non-conformance root cause diagnoses
          </p>
        </div>
        <button
          onClick={() => navigate('/investigations')}
          className="text-xs font-medium text-amber-700 hover:text-amber-800 transition-colors"
        >
          Investigation Workspace →
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="enterprise-table">
          <thead>
            <tr>
              <th>Investigation</th>
              <th>Component</th>
              <th>Machine</th>
              <th>Failure Mode</th>
              <th>Primary Cause</th>
              <th>Confidence</th>
              <th>Status</th>
              <th>Logged Date</th>
              <th className="text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            {investigations.map((inv) => (
              <tr 
                key={inv.investigation_id}
                className="cursor-pointer"
                onClick={() => navigate(`/investigations?comp=${inv.component_id}`)}
              >
                <td className="font-mono font-medium text-amber-800">{inv.investigation_id}</td>
                <td className="font-mono font-semibold text-slate-900">{inv.component_id}</td>
                <td className="font-mono text-slate-700">{inv.machine_id}</td>
                <td className="text-slate-700">{inv.failure_type}</td>
                <td className="font-medium text-slate-900">{inv.primary_root_cause}</td>
                <td className="font-mono font-medium text-slate-900">{inv.confidence}%</td>
                <td>
                  <StatusBadge status={inv.status || inv.severity} size="xs" />
                </td>
                <td className="text-slate-500 font-mono text-xs">{inv.created_at}</td>
                <td className="text-right">
                  <button className="text-slate-400 hover:text-slate-700 p-1">
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
