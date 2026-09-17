import React from 'react';

export default function StatusBadge({ status, size = 'sm', className = '' }) {
  const norm = String(status || '').toLowerCase();
  
  let styles = 'bg-[#F4F6F8] text-[#465563] border-[#D8E0E6]';
  let dotColor = 'bg-[#667685]';

  if (norm === 'critical' || norm === 'fail' || norm === 'overdue' || norm === 'high') {
    styles = 'bg-[#F9EBEB] text-[#C34B4B] border-[#F2CDCD] font-medium';
    dotColor = 'bg-[#C34B4B]';
  } else if (norm === 'warning' || norm === 'medium-high' || norm === 'medium') {
    styles = 'bg-[#FAF4E8] text-[#C58A20] border-[#F0DEC0] font-medium';
    dotColor = 'bg-[#C58A20]';
  } else if (norm === 'nominal' || norm === 'pass' || norm === 'completed' || norm === 'healthy' || norm === 'online' || norm === 'high confidence') {
    styles = 'bg-[#E9F5F0] text-[#23805A] border-[#C6E6D8] font-medium';
    dotColor = 'bg-[#23805A]';
  } else if (norm === 'info' || norm === 'running' || norm === 'investigated' || norm === 'standard') {
    styles = 'bg-[#F4F6F8] text-[#465563] border-[#D8E0E6] font-medium';
    dotColor = 'bg-[#667685]';
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
