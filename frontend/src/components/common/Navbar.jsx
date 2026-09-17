import React, { useState, useEffect } from 'react';
import { Search, Bell, Clock, Building2, User } from 'lucide-react';

export default function Navbar() {
  const [timeStr, setTimeStr] = useState('');

  useEffect(() => {
    const update = () => {
      const now = new Date();
      setTimeStr(now.toTimeString().split(' ')[0] + ' UTC');
    };
    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-14 bg-white border-b border-slate-200 px-6 flex items-center justify-between sticky top-0 z-30">
      {/* Left: Facility Selector & Search */}
      <div className="flex items-center gap-4 flex-1 max-w-xl">
        <div className="flex items-center gap-1.5 text-xs font-medium text-slate-700 bg-slate-50 border border-slate-200 px-2.5 py-1 rounded">
          <Building2 className="w-3.5 h-3.5 text-slate-500" />
          <span>Plant 01 (Precision CNC)</span>
        </div>

        <div className="relative flex-1">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search component (e.g. CNC-2847), machine ID, or work order..."
            className="w-full bg-white border border-slate-200 rounded pl-8 pr-3 py-1 text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-[#356B7A] font-mono transition-colors"
          />
        </div>
      </div>

      {/* Right: Telemetry Time, Alerts, Profile */}
      <div className="flex items-center gap-4">
        {/* Timestamp */}
        <div className="flex items-center gap-1.5 text-xs text-slate-500 font-mono">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span>{timeStr || '14:00:00 UTC'}</span>
        </div>

        {/* Notifications */}
        <button 
          className="relative p-1.5 rounded hover:bg-slate-100 text-slate-600 transition-colors"
          title="Active Alerts"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-[#C87916]" />
        </button>

        {/* User Info */}
        <div className="flex items-center gap-2 pl-3 border-l border-slate-200">
          <div className="w-6 h-6 rounded bg-[#E8F0F2] border border-[#D8E0E6] flex items-center justify-center text-[#356B7A] text-xs font-semibold">
            <User className="w-3.5 h-3.5 text-[#356B7A]" />
          </div>
          <div className="text-left hidden sm:block">
            <p className="text-xs font-medium text-slate-900 leading-tight">Quality Engineering</p>
            <p className="text-[10px] text-slate-500 leading-tight">Shift A · Operations</p>
          </div>
        </div>
      </div>
    </header>
  );
}
