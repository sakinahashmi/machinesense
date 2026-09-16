import React from 'react';

export default function StatusBadge({ status, size = 'sm', className = '' }) {
  const norm = String(status || '').toLowerCase();
  
  let styles = 'bg-slate-100 text-slate-700 border-slate-200';
  let dotColor = 'bg-slate-500';

  if (norm === 'critical' || norm === 'fail' || norm === 'overdue' || norm === 'high') {
    styles = 'bg-red-50 text-red-700 border-red-200 font-medium';
    dotColor = 'bg-red-600';
  } else if (norm === 'warning' || norm === 'medium-high' || norm === 'medium') {
    styles = 'bg-amber-50 text-amber-800 border-amber-200 font-medium';
    dotColor = 'bg-amber-600';
  } else if (norm === 'nominal' || norm === 'pass' || norm === 'completed' || norm === 'healthy' || norm === 'online' || norm === 'high confidence') {
    styles = 'bg-emerald-50 text-emerald-800 border-emerald-200 font-medium';
    dotColor = 'bg-emerald-600';
  } else if (norm === 'info' || norm === 'running' || norm === 'investigated' || norm === 'standard') {
    styles = 'bg-blue-50 text-blue-700 border-blue-200 font-medium';
    dotColor = 'bg-blue-600';
  }

  const sizeClasses = size === 'xs' 
    ? 'px-1.5 py-0.5 text-[11px]' 
    : size === 'lg' 
      ? 'px-2.5 py-1 text-sm' 
      : 'px-2 py-0.5 text-xs';

  return (
    <span className={`inline-flex items-center gap-1.5 rounded border ${sizeClasses} ${styles} ${className}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dotColor}`} />
      <span>{status}</span>
    </span>
  );
}
