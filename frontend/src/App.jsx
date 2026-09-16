import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/common/Sidebar';
import Navbar from './components/common/Navbar';
import DashboardPage from './pages/DashboardPage';
import InvestigationsPage from './pages/InvestigationsPage';
import MachinesPage from './pages/MachinesPage';
import MaintenancePage from './pages/MaintenancePage';
import HistoricalCasesPage from './pages/HistoricalCasesPage';
import AIInsightsPage from './pages/AIInsightsPage';

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-[#F5F6F8] text-slate-900 font-sans antialiased">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0">
          <Navbar />
          <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/investigations" element={<InvestigationsPage />} />
              <Route path="/machines" element={<MachinesPage />} />
              <Route path="/maintenance" element={<MaintenancePage />} />
              <Route path="/historical-cases" element={<HistoricalCasesPage />} />
              <Route path="/insights" element={<AIInsightsPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}
