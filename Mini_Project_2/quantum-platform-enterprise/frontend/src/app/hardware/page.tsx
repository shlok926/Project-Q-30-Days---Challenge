"use client";

import React, { useState, useEffect } from 'react';
import { Cpu, Server, Activity, CheckCircle, AlertTriangle } from 'lucide-react';

export default function HardwarePage() {
  const [providers, setProviders] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProviders = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/v1/analytics/providers');
        if (!res.ok) throw new Error("Failed to fetch hardware analytics");
        const data = await res.json();
        setProviders(data);
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchProviders();
    // Refresh every 10 seconds to show "live" data
    const interval = setInterval(fetchProviders, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading && !providers) return <div className="text-gray-400 p-8">Loading Quantum Nodes...</div>;
  if (error) return <div className="text-rose-400 p-8 bg-rose-500/10 border border-rose-500/20 rounded-md">Error: {error}</div>;

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-semibold text-white mb-1">Hardware & Nodes</h1>
        <p className="text-gray-400 text-sm">View status of all connected quantum backends and simulators.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* IBM Quantum Node */}
        <div className="bg-[#111] border border-[#222] rounded-lg p-6 relative overflow-hidden group hover:border-[#333] transition-all">
          <div className="absolute top-0 right-0 p-4">
            {providers?.ibm_quantum?.health_status === 'operational' ? (
              <span className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded">
                <CheckCircle className="w-3 h-3" /> Online
              </span>
            ) : (
              <span className="flex items-center gap-1.5 text-xs text-rose-400 bg-rose-500/10 px-2 py-1 rounded">
                <AlertTriangle className="w-3 h-3" /> Offline
              </span>
            )}
          </div>
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 bg-blue-500/10 rounded-lg border border-blue-500/20">
              <Cpu className="w-6 h-6 text-blue-400" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">IBM Quantum</h2>
              <p className="text-xs text-gray-400">Production QPU Cluster</p>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center border-b border-[#222] pb-2">
              <span className="text-sm text-gray-400">Target Backend</span>
              <span className="text-sm text-gray-200 font-mono">ibmq_qasm_simulator</span>
            </div>
            <div className="flex justify-between items-center border-b border-[#222] pb-2">
              <span className="text-sm text-gray-400">Usage Load</span>
              <div className="flex items-center gap-3">
                <div className="w-24 h-1.5 bg-[#222] rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500" style={{ width: `${providers?.ibm_quantum?.usage_percentage || 0}%` }}></div>
                </div>
                <span className="text-sm text-gray-200">{providers?.ibm_quantum?.usage_percentage}%</span>
              </div>
            </div>
            <div className="flex justify-between items-center pb-2">
              <span className="text-sm text-gray-400">Average Queue Time</span>
              <span className="text-sm text-gray-200">{providers?.ibm_quantum?.average_queue_time || 'N/A'}</span>
            </div>
          </div>
        </div>

        {/* Local Aer Simulator Node */}
        <div className="bg-[#111] border border-[#222] rounded-lg p-6 relative overflow-hidden group hover:border-[#333] transition-all">
          <div className="absolute top-0 right-0 p-4">
            {providers?.aer_simulator?.health_status === 'operational' ? (
              <span className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded">
                <CheckCircle className="w-3 h-3" /> Online
              </span>
            ) : (
              <span className="flex items-center gap-1.5 text-xs text-amber-400 bg-amber-500/10 px-2 py-1 rounded">
                <Activity className="w-3 h-3 animate-pulse" /> Standby
              </span>
            )}
          </div>
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 bg-purple-500/10 rounded-lg border border-purple-500/20">
              <Server className="w-6 h-6 text-purple-400" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Local Aer Simulator</h2>
              <p className="text-xs text-gray-400">In-Memory Engine</p>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center border-b border-[#222] pb-2">
              <span className="text-sm text-gray-400">Target Backend</span>
              <span className="text-sm text-gray-200 font-mono">aer_simulator</span>
            </div>
            <div className="flex justify-between items-center border-b border-[#222] pb-2">
              <span className="text-sm text-gray-400">Usage Load</span>
              <div className="flex items-center gap-3">
                <div className="w-24 h-1.5 bg-[#222] rounded-full overflow-hidden">
                  <div className="h-full bg-purple-500" style={{ width: `${providers?.aer_simulator?.usage_percentage || 0}%` }}></div>
                </div>
                <span className="text-sm text-gray-200">{providers?.aer_simulator?.usage_percentage}%</span>
              </div>
            </div>
            <div className="flex justify-between items-center pb-2">
              <span className="text-sm text-gray-400">Average Queue Time</span>
              <span className="text-sm text-gray-200">{providers?.aer_simulator?.average_queue_time || '0s'}</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
