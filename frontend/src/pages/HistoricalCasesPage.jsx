import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Search } from 'lucide-react';

const ROOT_CAUSES = [
  'ALL',
  'Tool Wear',
  'Excessive Vibration',
  'Incorrect Feed Rate',
  'Coolant Temperature Variation',
  'Machine Calibration Drift',
  'Tool Offset Error',
  'Maintenance Overdue'
];

export default function HistoricalCasesPage() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedCause, setSelectedCause] = useState('ALL');

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const res = await api.getHistoricalCases({
          search: search || undefined,
          root_cause: selectedCause === 'ALL' ? undefined : selectedCause
        });
        setCases(res);
      } catch (err) {
        console.error('Failed to load historical cases:', err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [search, selectedCause]);

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900">
            Historical Incident Knowledge Base
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Archive of historical root cause investigations, physical evidence, and corrective resolutions
          </p>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by symptom, tool, machine..."
            className="bg-white border border-slate-300 rounded pl-8 pr-2.5 py-1 text-xs font-mono text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-[#356B7A] w-64"
          />
        </div>
      </div>

      {/* Cause Filter Buttons */}
      <div className="flex items-center gap-1 overflow-x-auto pb-1 text-xs">
        <span className="text-slate-500 font-medium mr-1 text-xs">Filter by Cause:</span>
        {ROOT_CAUSES.map((rc) => (
          <button
            key={rc}
            onClick={() => setSelectedCause(rc)}
            className={`px-2.5 py-1 rounded text-xs transition-colors whitespace-nowrap ${
              selectedCause === rc
                ? 'bg-[#356B7A] text-white font-semibold'
                : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
            }`}
          >
            {rc}
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="enterprise-card">
        <div className="p-4 border-b border-slate-200">
          <h3 className="text-sm font-bold text-slate-900">
            Incident Records ({cases.length} Records)
          </h3>
        </div>

        <div className="overflow-x-auto">
          <table className="enterprise-table">
            <thead>
              <tr>
                <th>Case ID</th>
                <th>Machine</th>
                <th>Failure Mode</th>
                <th>Identified Root Cause</th>
                <th>Physical Evidence</th>
                <th>Corrective Action Taken</th>
                <th className="text-right">MTTR</th>
              </tr>
            </thead>
            <tbody>
              {cases.map((c) => (
                <tr key={c.case_id}>
                  <td className="font-mono font-medium text-[#356B7A]">{c.case_id}</td>
                  <td className="font-mono font-semibold text-slate-900">{c.machine_id}</td>
                  <td className="text-slate-700">{c.failure_type}</td>
                  <td className="font-medium text-slate-900">{c.root_cause}</td>
                  <td className="text-slate-600 max-w-xs truncate" title={c.evidence}>
                    {c.evidence}
                  </td>
                  <td className="text-slate-700 max-w-xs truncate" title={c.corrective_action}>
                    {c.corrective_action}
                  </td>
                  <td className="text-right font-mono text-slate-500 text-xs">
                    {c.resolution_time}h
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
