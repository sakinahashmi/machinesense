import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  SearchCode, 
  Cpu, 
  Wrench, 
  Archive, 
  BarChart3,
  Factory
} from 'lucide-react';

const NAV_ITEMS = [
  { to: '/', label: 'Overview', icon: LayoutDashboard },
  { to: '/investigations', label: 'Investigations', icon: SearchCode },
  { to: '/machines', label: 'Machines', icon: Cpu },
  { to: '/maintenance', label: 'Maintenance', icon: Wrench },
  { to: '/historical-cases', label: 'Historical Cases', icon: Archive },
  { to: '/insights', label: 'Analysis Insights', icon: BarChart3 },
];

export default function Sidebar() {
  return (
    <aside className="w-56 bg-[#0F172A] border-r border-slate-800 flex flex-col shrink-0 min-h-screen select-none">
      {/* Brand Header */}
      <div className="h-14 px-4 border-b border-slate-800 flex items-center gap-2.5">
        <div className="w-7 h-7 rounded bg-amber-600 flex items-center justify-center text-white font-bold text-sm tracking-wider">
          M
        </div>
        <div>
          <span className="text-sm font-bold text-white tracking-tight">MachineSense</span>
          <span className="text-[10px] text-slate-400 block font-normal leading-none mt-0.5">Manufacturing RCA</span>
        </div>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 py-3 px-2 space-y-0.5">
        <div className="px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
          Navigation
        </div>

        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) => `
                flex items-center gap-2.5 px-3 py-2 rounded text-xs font-medium transition-colors
                ${isActive 
                  ? 'bg-slate-800 text-white font-semibold' 
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }
              `}
            >
              <Icon className="w-4 h-4 shrink-0 text-slate-400" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>

      {/* Facility Information */}
      <div className="p-3 border-t border-slate-800 text-[11px] text-slate-400">
        <div className="flex items-center gap-2 mb-1">
          <Factory className="w-3.5 h-3.5 text-amber-500" />
          <span className="text-slate-300 font-medium truncate">Facility 01 - CNC Line</span>
        </div>
        <div className="flex items-center justify-between text-[10px] text-slate-400 pl-5.5">
          <span>Telemetry Stream</span>
          <span className="text-emerald-400 font-medium">Online</span>
        </div>
      </div>
    </aside>
  );
}
