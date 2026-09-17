import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../services/api';
import InvestigationHeader from '../components/investigation/InvestigationHeader';
import RootCauseRankList from '../components/investigation/RootCauseRankList';
import EvidencePanel from '../components/investigation/EvidencePanel';
import TrendCharts from '../components/investigation/TrendCharts';
import HistoricalMatchCard from '../components/investigation/HistoricalMatchCard';
import ActionMatrix from '../components/investigation/ActionMatrix';
import InvestigationSummaryBox from '../components/investigation/InvestigationSummaryBox';
import LoadingOverlay from '../components/common/LoadingOverlay';
import { 
  SearchCode, 
  Play, 
  AlertTriangle, 
  FileText
} from 'lucide-react';

const MACHINES_LIST = [
  'CNC-01', 'CNC-02', 'CNC-03', 'CNC-04',
  'CNC-05', 'CNC-06', 'CNC-07', 'CNC-08'
];

const FAILURE_TYPES = [
  'Dimensional Inspection Failure',
  'Surface Roughness & Chattering',
  'Dimensional Undersize',
  'Bore Taper Defect',
  'Positional True Position Error'
];

export default function InvestigationsPage() {
  const [searchParams] = useSearchParams();

  // Form State
  const [componentId, setComponentId] = useState('CNC-2847');
  const [machineId, setMachineId] = useState('CNC-07');
  const [failureType, setFailureType] = useState('Dimensional Inspection Failure');

  // Analysis State
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [selectedCauseIndex, setSelectedCauseIndex] = useState(0);
  const [error, setError] = useState(null);

  const runAnalysis = async (comp = componentId, mId = machineId, fType = failureType) => {
    setIsAnalyzing(true);
    setError(null);

    setTimeout(async () => {
      try {
        const data = await api.analyzeFailure({
          componentId: comp,
          machineId: mId,
          failureType: fType,
        });
        setResult(data);
        setSelectedCauseIndex(0);
      } catch (err) {
        console.error('Analysis failed:', err);
        setError('Failed to complete root cause analysis. Please verify backend connectivity.');
      } finally {
        setIsAnalyzing(false);
      }
    }, 450);
  };

  const handleLoadDemo = () => {
    setComponentId('CNC-2847');
    setMachineId('CNC-07');
    setFailureType('Dimensional Inspection Failure');
    runAnalysis('CNC-2847', 'CNC-07', 'Dimensional Inspection Failure');
  };

  useEffect(() => {
    const compParam = searchParams.get('comp');
    if (compParam) {
      setComponentId(compParam);
      runAnalysis(compParam, 'CNC-07', 'Dimensional Inspection Failure');
    } else {
      runAnalysis('CNC-2847', 'CNC-07', 'Dimensional Inspection Failure');
    }
  }, []);

  return (
    <div className="space-y-5">
      <LoadingOverlay isAnalyzing={isAnalyzing} />

      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900">
            Root Cause Investigation
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Analyze process, equipment, inspection and maintenance data associated with a failed component.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleLoadDemo}
            className="btn-secondary text-xs"
          >
            <FileText className="w-3.5 h-3.5 text-slate-500" />
            <span>Load Demo Case (CNC-2847)</span>
          </button>
        </div>
      </div>

      {/* Investigation Input Form */}
      <div className="enterprise-card p-4">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3">
          Investigation Parameters
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              Component ID
            </label>
            <input
              type="text"
              value={componentId}
              onChange={(e) => setComponentId(e.target.value)}
              placeholder="e.g. CNC-2847"
              className="w-full bg-white border border-slate-300 rounded px-2.5 py-1.5 text-xs font-mono text-slate-900 focus:outline-none focus:border-[#356B7A]"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              CNC Machine
            </label>
            <select
              value={machineId}
              onChange={(e) => setMachineId(e.target.value)}
              className="w-full bg-white border border-slate-300 rounded px-2.5 py-1.5 text-xs font-mono text-slate-900 focus:outline-none focus:border-[#356B7A]"
            >
              {MACHINES_LIST.map((m) => (
                <option key={m} value={m}>
                  {m} {m === 'CNC-07' ? '(Hermle 5-Axis - Line 1)' : ''}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              Failure Mode
            </label>
            <select
              value={failureType}
              onChange={(e) => setFailureType(e.target.value)}
              className="w-full bg-white border border-slate-300 rounded px-2.5 py-1.5 text-xs text-slate-900 focus:outline-none focus:border-[#356B7A]"
            >
              {FAILURE_TYPES.map((f) => (
                <option key={f} value={f}>
                  {f}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={() => runAnalysis()}
              disabled={isAnalyzing}
              className="btn-primary w-full justify-center text-xs py-2 disabled:opacity-50"
            >
              <Play className="w-3.5 h-3.5 fill-white" />
              <span>{isAnalyzing ? 'Processing...' : 'Analyze Investigation'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="p-3 rounded bg-[#F9EBEB] border border-[#F2CDCD] text-xs text-[#C34B4B] flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-[#C34B4B] shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Investigation Results */}
      {result && (
        <div className="space-y-5">
          {/* Header */}
          <InvestigationHeader investigation={result} />

          {/* Root Cause Ranking & Evidence Panel */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
            <div className="lg:col-span-5">
              <RootCauseRankList
                rankings={result.root_cause_ranking || []}
                selectedIndex={selectedCauseIndex}
                onSelectCause={(idx) => setSelectedCauseIndex(idx)}
              />
            </div>

            <div className="lg:col-span-7">
              <EvidencePanel
                rootCause={result.root_cause_ranking?.[selectedCauseIndex]}
              />
            </div>
          </div>

          {/* Correlated Telemetry Trend Charts */}
          <TrendCharts trends={result.trends || []} />

          {/* Similar Historical Cases */}
          <HistoricalMatchCard matches={result.historical_matches || []} />

          {/* Action Matrix */}
          <ActionMatrix actions={result.corrective_actions || []} />

          {/* Executive Summary Report */}
          <InvestigationSummaryBox summary={result.investigation_summary} />
        </div>
      )}
    </div>
  );
}
