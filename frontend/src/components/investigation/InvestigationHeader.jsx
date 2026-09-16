import React, { useState } from 'react';
import StatusBadge from '../common/StatusBadge';
import { Copy, Check, Printer } from 'lucide-react';

export default function InvestigationHeader({ investigation }) {
  const [copied, setCopied] = useState(false);

  const insp = investigation?.inspection_details || {};

  const handleCopySummary = () => {
    if (!investigation?.investigation_summary) return;
    const text = `MACHINESENSE INVESTIGATION REPORT\n` +
      `ID: ${investigation.investigation_id}\n` +
      `Component: ${investigation.component_id} | Machine: ${investigation.machine_id}\n` +
      `Failure Mode: ${investigation.failure_type}\n` +
      `Specification: ${insp.expected_value || 25.00} mm ± ${insp.tolerance || 0.10} mm | Measured: ${insp.actual_value || 25.42} mm (Deviation: +${insp.deviation || 0.420} mm)\n` +
      `Primary Root Cause: ${investigation.investigation_summary.primary_root_cause} (${investigation.investigation_summary.confidence}% confidence)\n` +
      `\n${investigation.investigation_summary.technical_narrative}`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="enterprise-card p-5 border-l-4 border-l-red-600">
      <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4">
        {/* Left: Metadata & Inspection Data */}
        <div className="space-y-3 flex-1">
          <div className="flex items-center gap-2.5 flex-wrap">
            <span className="font-mono text-xs font-semibold text-slate-800 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded">
              {investigation.investigation_id || 'INV-2026-001'}
            </span>
            <StatusBadge status={investigation.severity || 'Critical'} size="xs" />
            <StatusBadge status={investigation.status || 'Investigated'} size="xs" />
            <span className="text-xs text-slate-500 font-mono">
              Logged: {investigation.created_at || '2026-09-15 14:02:11 UTC'}
            </span>
          </div>

          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <span>Component {investigation.component_id}</span>
              <span className="text-slate-400 font-normal">/</span>
              <span className="text-slate-700">{investigation.machine_id}</span>
            </h2>
            <p className="text-xs font-medium text-slate-600 mt-0.5">
              Failure Mode: <span className="text-red-700 font-semibold">{investigation.failure_type}</span>
            </p>
          </div>

          {/* Inspection Parameter Summary Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-3 rounded border border-slate-200 text-xs">
            <div>
              <span className="text-[11px] text-slate-500 block uppercase">Dimension Name</span>
              <span className="font-medium text-slate-900">{insp.dimension_name || 'Outer Diameter'}</span>
            </div>
            <div>
              <span className="text-[11px] text-slate-500 block uppercase">Specification</span>
              <span className="font-mono font-medium text-slate-900">
                {insp.expected_value || 25.00} ± {insp.tolerance || 0.10} mm
              </span>
            </div>
            <div>
              <span className="text-[11px] text-slate-500 block uppercase">Measured Value</span>
              <span className="font-mono font-bold text-red-700">
                {insp.actual_value || 25.42} mm
              </span>
            </div>
            <div>
              <span className="text-[11px] text-slate-500 block uppercase">Deviation</span>
              <span className="font-mono font-bold text-red-700">
                +{insp.deviation || 0.420} mm
              </span>
            </div>
          </div>
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={handleCopySummary}
            className="btn-secondary text-xs"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-slate-500" />}
            <span>{copied ? 'Copied' : 'Copy Report'}</span>
          </button>
          
          <button
            onClick={() => window.print()}
            className="btn-secondary text-xs p-2"
            title="Print Report"
          >
            <Printer className="w-3.5 h-3.5 text-slate-500" />
          </button>
        </div>
      </div>
    </div>
  );
}
