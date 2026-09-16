import React, { useState, useEffect } from 'react';
import { Loader2, CheckCircle2 } from 'lucide-react';

const STEPS = [
  "Connecting to CNC telemetry stream...",
  "Analyzing spindle vibration harmonics & cutting force...",
  "Evaluating tool wear accumulation & cycle thresholds...",
  "Querying historical failure cases...",
  "Synthesizing root cause correlation matrix..."
];

export default function LoadingOverlay({ isAnalyzing = false }) {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    if (!isAnalyzing) {
      setActiveStep(0);
      return;
    }
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 280);
    return () => clearInterval(interval);
  }, [isAnalyzing]);

  if (!isAnalyzing) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-[2px] flex items-center justify-center p-4">
      <div className="bg-white border border-slate-300 rounded-md p-6 max-w-md w-full shadow-lg">
        <div className="flex items-center gap-3 mb-4">
          <Loader2 className="w-5 h-5 text-amber-600 animate-spin" />
          <div>
            <h3 className="text-sm font-semibold text-slate-900">
              Processing Root Cause Investigation
            </h3>
            <p className="text-xs text-slate-500">
              Analyzing sensor telemetry, process parameters, and maintenance records
            </p>
          </div>
        </div>

        {/* Step Progress List */}
        <div className="space-y-2 bg-slate-50 rounded p-3 border border-slate-200">
          {STEPS.map((label, idx) => {
            const isCurrent = idx === activeStep;
            const isCompleted = idx < activeStep;

            return (
              <div 
                key={idx} 
                className={`flex items-center gap-2 text-xs transition-colors ${
                  isCurrent ? 'text-amber-800 font-medium' : isCompleted ? 'text-emerald-700' : 'text-slate-400'
                }`}
              >
                {isCompleted ? (
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                ) : (
                  <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${isCurrent ? 'bg-amber-600 animate-pulse' : 'bg-slate-300'}`} />
                )}
                <span className="truncate">{label}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
