"use client";

import React, { useState, useEffect } from 'react';
import { Activity, Database, Zap, Clock } from 'lucide-react';

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/v1/analytics/overview');
        if (res.ok) {
          const data = await res.json();
          setMetrics(data);
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000); // Polling every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-semibold text-white mb-1">Telemetry & Logs</h1>
        <p className="text-gray-400 text-sm">System metrics and live execution telemetry from the Quantum Engine.</p>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-[#111] border border-[#222] rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2 text-blue-400">
            <Activity className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Total Executions</span>
          </div>
          <p className="text-2xl font-bold text-white">{metrics?.total_experiments || 0}</p>
        </div>
        <div className="bg-[#111] border border-[#222] rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2 text-emerald-400">
            <Database className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Success Rate</span>
          </div>
          <p className="text-2xl font-bold text-white">{metrics?.success_rate ? `${metrics.success_rate.toFixed(1)}%` : '0%'}</p>
        </div>
        <div className="bg-[#111] border border-[#222] rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2 text-purple-400">
            <Zap className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Avg Fidelity</span>
          </div>
          <p className="text-2xl font-bold text-white">{metrics?.average_fidelity ? `${(metrics.average_fidelity * 100).toFixed(1)}%` : 'N/A'}</p>
        </div>
        <div className="bg-[#111] border border-[#222] rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2 text-amber-400">
            <Clock className="w-4 h-4" />
            <span className="text-xs font-semibold uppercase tracking-wider">Active Jobs</span>
          </div>
          <p className="text-2xl font-bold text-white">{metrics?.active_jobs || 0}</p>
        </div>
      </div>

      {/* Logs Window */}
      <div className="bg-[#0a0a0a] border border-[#222] rounded-lg p-4 h-[400px] flex flex-col">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-sm font-semibold text-gray-300">Live Engine Logs</h2>
          <span className="flex items-center gap-1.5 text-[10px] text-emerald-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Streaming
          </span>
        </div>
        <div className="flex-1 overflow-y-auto font-mono text-xs space-y-2 p-2 bg-black rounded border border-[#111]">
          {loading ? (
            <div className="text-gray-500">Connecting to log stream...</div>
          ) : (
            <>
              <div className="text-gray-400"><span className="text-blue-400">[INFO]</span> {new Date().toISOString()} - Telemetry stream connected.</div>
              <div className="text-gray-400"><span className="text-blue-400">[INFO]</span> {new Date().toISOString()} - Loaded {metrics?.total_experiments || 0} historical records.</div>
              {metrics?.active_jobs > 0 && (
                <div className="text-gray-400"><span className="text-amber-400">[WARN]</span> {new Date().toISOString()} - Processing {metrics.active_jobs} active queue items...</div>
              )}
              {metrics?.recent_activity?.map((activity: any, idx: number) => (
                <div key={idx} className="text-gray-400">
                  <span className={activity.status === 'COMPLETED' ? 'text-emerald-400' : (activity.status === 'FAILED' ? 'text-rose-400' : 'text-purple-400')}>
                    [{activity.status}]
                  </span> {activity.timestamp || new Date().toISOString()} - Experiment {activity.name || activity.id} processed.
                </div>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
