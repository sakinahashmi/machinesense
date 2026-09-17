import React, { useState } from 'react';
import { Copy, Check } from 'lucide-react';

export default function InvestigationSummaryBox({ summary }) {
  const [copied, setCopied] = useState(false);

  if (!summary) return null;

  const handleCopy = () => {
    const text = `INVESTIGATION SUMMARY REPORT\n` +
      `Component: ${summary.component_id} | Machine: ${summary.machine_id}\n` +
      `Failure: ${summary.failure_type}\n` +
      `Finding: ${summary.primary_root_cause} (${summary.confidence}% Confidence)\n\n` +
      `Key Evidence:\n${summary.key_evidence.map((e, i) => `${i + 1}. ${e}`).join('\n')}\n\n` +
      `Immediate Action: ${summary.recommended_immediate_action}\n` +
      `Preventive Action: ${summary.preventive_recommendation}\n\n` +
      `Technical Assessment:\n${summary.technical_narrative}`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="enterprise-card p-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-200">
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Investigation Summary & Engineering Assessment
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Synthesized report for quality records and shift handovers
          </p>
        </div>

        <button
          onClick={handleCopy}
          className="btn-secondary text-xs"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-[#23805A]" /> : <Copy className="w-3.5 h-3.5 text-slate-500" />}
          <span>{copied ? 'Copied' : 'Copy Summary'}</span>
        </button>
      </div>

      {/* Core Finding */}
      <div className="p-3 bg-[#E8F0F2] border border-[#B8D2D9] rounded text-xs mb-4">
        <span className="text-[#356B7A] font-bold uppercase text-[11px] block mb-0.5">
          Primary Diagnostic Finding
        </span>
        <p className="text-slate-900 font-medium leading-relaxed">
          <strong>{summary.primary_root_cause}</strong> is identified as the most probable cause ({summary.confidence}% confidence) for the dimensional failure on component {summary.component_id}.
        </p>
      </div>

      {/* Key Evidence Points */}
      <div className="mb-4">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
          Supporting Diagnostic Evidence
        </h4>
        <ul className="space-y-1.5 text-xs text-slate-700">
          {summary.key_evidence?.map((item, idx) => (
            <li key={idx} className="flex items-start gap-2 bg-slate-50 p-2 rounded border border-slate-200">
              <span className="text-slate-400 font-mono text-[11px] font-bold mt-0.5">{idx + 1}.</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Technical Narrative */}
      <div className="p-3.5 bg-slate-50 rounded border border-slate-200 text-xs text-slate-800 leading-relaxed mb-4">
        <span className="text-[11px] font-bold uppercase text-slate-500 block mb-1">
          Technical Physics-of-Failure Analysis
        </span>
        <p>{summary.technical_narrative}</p>
      </div>

      {/* Immediate vs Preventive Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        <div className="p-3 rounded bg-slate-50 border border-slate-200">
          <span className="text-[11px] font-bold uppercase text-[#C34B4B] block mb-1">
            Immediate Containment Action
          </span>
          <p className="text-slate-800 font-medium">{summary.recommended_immediate_action}</p>
        </div>

        <div className="p-3 rounded bg-slate-50 border border-slate-200">
          <span className="text-[11px] font-bold uppercase text-slate-700 block mb-1">
            Preventive Process Recommendation
          </span>
          <p className="text-slate-800 font-medium">{summary.preventive_recommendation}</p>
        </div>
      </div>
    </div>
  );
}
