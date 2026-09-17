import React from 'react';
import StatusBadge from '../common/StatusBadge';

export default function RootCauseRankList({ rankings = [], selectedIndex = 0, onSelectCause }) {
  return (
    <div className="enterprise-card">
      <div className="p-4 border-b border-slate-200 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Root Cause Ranking
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Probable root causes ranked by multi-signal correlation score
          </p>
        </div>
        <span className="text-xs text-slate-500">
          Select row to view evidence
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="enterprise-table">
          <thead>
            <tr>
              <th className="w-12 text-center">Rank</th>
              <th>Potential Cause</th>
              <th>Confidence</th>
              <th>Evidence Strength</th>
              <th className="text-right">Status</th>
            </tr>
          </thead>
          <tbody>
            {rankings.map((cause, idx) => {
              const isSelected = idx === selectedIndex;
              const isTop = idx === 0;

              return (
                <tr
                  key={cause.root_cause}
                  onClick={() => onSelectCause(idx)}
                  className={`cursor-pointer transition-colors ${
                    isSelected ? 'bg-[#E8F0F2] font-medium' : ''
                  }`}
                >
                  <td className="text-center font-mono font-semibold text-slate-700">
                    #{idx + 1}
                  </td>
                  <td>
                    <div className="flex items-center gap-2">
                      <span className={`text-slate-900 ${isTop ? 'font-bold' : 'font-medium'}`}>
                        {cause.root_cause}
                      </span>
                      {isTop && (
                        <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-[#E8F0F2] text-[#356B7A] border border-[#B8D2D9]">
                          Primary
                        </span>
                      )}
                    </div>
                  </td>
                  <td>
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
                        <div
                          className={`h-full ${
                            isTop ? 'bg-[#356B7A]' : 'bg-[#667685]'
                          }`}
                          style={{ width: `${cause.confidence}%` }}
                        />
                      </div>
                      <span className="font-mono text-xs font-semibold text-slate-900">
                        {cause.confidence}%
                      </span>
                    </div>
                  </td>
                  <td className="text-xs text-slate-600">
                    {cause.confidence_level === 'HIGH CONFIDENCE' ? (
                      <span className="text-[#C34B4B] font-medium">Strong</span>
                    ) : cause.confidence_level === 'MEDIUM-HIGH' || cause.confidence_level === 'MEDIUM' ? (
                      <span className="text-[#C58A20] font-medium">Supporting</span>
                    ) : (
                      <span className="text-slate-500 font-normal">Weak</span>
                    )}
                  </td>
                  <td className="text-right">
                    <StatusBadge status={cause.severity} size="xs" />
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
