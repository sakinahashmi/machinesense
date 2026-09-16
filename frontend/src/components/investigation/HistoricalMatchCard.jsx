import React from 'react';

export default function HistoricalMatchCard({ matches = [] }) {
  return (
    <div className="enterprise-card">
      <div className="p-4 border-b border-slate-200 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Similar Historical Failure Cases
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Vectorized similarity matching against historical plant incident records
          </p>
        </div>
        <span className="text-xs font-mono text-slate-500">
          {matches.length} Matches Found
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="enterprise-table">
          <thead>
            <tr>
              <th>Case ID</th>
              <th>Machine</th>
              <th>Failure Mode</th>
              <th>Identified Cause</th>
              <th>Similarity</th>
              <th>Historical Corrective Action</th>
              <th className="text-right">MTTR</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((item) => (
              <tr key={item.case_id}>
                <td className="font-mono font-medium text-amber-800">{item.case_id}</td>
                <td className="font-mono text-slate-800">{item.machine_id}</td>
                <td className="text-slate-600">{item.failure_type}</td>
                <td className="font-medium text-slate-900">{item.root_cause}</td>
                <td>
                  <span className="font-mono font-bold text-slate-900 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">
                    {item.similarity_score}%
                  </span>
                </td>
                <td className="text-slate-700 max-w-xs truncate" title={item.corrective_action}>
                  {item.corrective_action}
                </td>
                <td className="text-right font-mono text-slate-500 text-xs">
                  {item.resolution_time}h
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
