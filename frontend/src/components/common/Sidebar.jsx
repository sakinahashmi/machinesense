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
    <aside className="sidebar-container w-56 flex flex-col shrink-0 min-h-screen select-none">
      {/* Brand Header */}
      <div className="sidebar-header h-14 px-4 flex items-center gap-2.5">
        <div className="w-7 h-7 rounded bg-[#356B7A] flex items-center justify-center text-white font-bold text-sm tracking-wider shadow-sm">
          M
        </div>
        <div>
          <span className="sidebar-title text-sm font-bold tracking-tight">MachineSense</span>
          <span className="sidebar-subtitle text-[10px] block font-normal leading-none mt-0.5">Manufacturing RCA</span>
        </div>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 py-3 px-2 space-y-0.5">
        <div className="sidebar-section-heading px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider">
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
                sidebar-nav-link flex items-center gap-2.5 px-3 py-2 rounded text-xs font-medium
                ${isActive ? 'active' : ''}
              `}
            >
              <Icon className="sidebar-icon w-4 h-4 shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>

      {/* Facility Information */}
      <div className="sidebar-footer p-3 text-[11px]">
        <div className="flex items-center gap-2 mb-1">
          <Factory className="w-3.5 h-3.5 text-slate-400" />
          <span className="sidebar-facility-name font-medium truncate">Facility 01 - CNC Line</span>
        </div>
        <div className="flex items-center justify-between text-[10px] pl-5.5">
          <span>Telemetry Stream</span>
          <span className="text-[#23805A] font-medium">Online</span>
        </div>
      </div>
    </aside>
  );
}
