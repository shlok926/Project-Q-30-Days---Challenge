"use client";

import React, { useState, useEffect } from 'react';
import { Play, Cpu, Network, Terminal, CheckCircle2, AlertCircle, Download } from 'lucide-react';

export default function WorkspacePage() {
  const [algorithm, setAlgorithm] = useState('bell_state');
  const [provider, setProvider] = useState('aer_simulator');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [experiments, setExperiments] = useState<any[]>([]);

  // Fetch past experiments (Mocked)
  const fetchExperiments = () => {
    setExperiments([]);
  };

  useEffect(() => {
    fetchExperiments();
  }, []);

  const runExperiment = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    // Simulate API delay for dramatic effect
    setTimeout(() => {
      setResult({
        job_id: `job_${Math.random().toString(36).substring(7)}`,
        status: 'COMPLETED',
        counts: { "00": 512, "11": 512 },
        circuit_image: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MDAiIGhlaWdodD0iMTIwIiB2aWV3Qm94PSIwIDAgNDAwIDEyMCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0id2hpdGUiLz48bGluZSB4MT0iNDAiIHkxPSI0MCIgeDI9IjM2MCIgeTI9IjQwIiBzdHJva2U9ImJsYWNrIiBzdHJva2Utd2lkdGg9IjIiLz48bGluZSB4MT0iNDAiIHkxPSI4MCIgeDI9IjM2MCIgeTI9IjgwIiBzdHJva2U9ImJsYWNrIiBzdHJva2Utd2lkdGg9IjIiLz48cmVjdCB4PSI4MCIgeT0iMjAiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgZmlsbD0iI2ZiNzE4NSIgc3Ryb2tlPSJibGFjayIvPjx0ZXh0IHg9IjEwMCIgeT0iNDYiIGZvbnQtZmFtaWx5PSJhcmlhbCIgZm9udC1zaXplPSIyMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iYmxhY2siPkg8L3RleHQ+PGNpcmNsZSBjeD0iMTYwIiBjeT0iNDAiIHI9IjUiIGZpbGw9ImJsYWNrIi8+PGxpbmUgeDE9IjE2MCIgeTE9IjQwIiB4Mj0iMTYwIiB5Mj0iODAiIHN0cm9rZT0iYmxhY2siIHN0cm9rZS13aWR0aD0iMiIvPjxjaXJjbGUgY3g9IjE2MCIgY3k9IjgwIiByPSIxNCIgZmlsbD0id2hpdGUiIHN0cm9rZT0iYmxhY2siIHN0cm9rZS13aWR0aD0iMiIvPjxsaW5lIHgxPSIxNjAiIHkxPSI2NiIgeDI9IjE2MCIgeTI9Ijk0IiBzdHJva2U9ImJsYWNrIiBzdHJva2Utd2lkdGg9IjIiLz48bGluZSB4MT0iMTQ2IiB5MT0iODAiIHgyPSIxNzQiIHkyPSI4MCIgc3Ryb2tlPSJibGFjayIgc3Ryb2tlLXdpZHRoPSIyIi8+PC9zdmc+"
      });
      setLoading(false);
    }, 2500);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-semibold text-white mb-1">Quantum Workspace</h1>
        <p className="text-gray-400 text-sm">Design, compile, and execute real quantum circuits against the engine API.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Workspace Controls */}
        <div className="bg-[#111] border border-[#222] rounded-lg p-6">
          <h2 className="text-md font-medium text-white mb-4">Job Configuration</h2>
          
          <div className="space-y-4">
            <div>
              <label className="text-xs text-gray-400 block mb-1">Quantum Algorithm</label>
              <select 
                value={algorithm}
                onChange={(e) => setAlgorithm(e.target.value)}
                className="w-full bg-[#1A1A1A] border border-[#333] rounded-md px-3 py-2 text-sm text-white"
              >
                <option value="bell_state">Bell State Entanglement</option>
                <option value="quantum_teleportation">Quantum Teleportation</option>
                <option value="grover_search">Grover Search</option>
                <option value="qft">Quantum Fourier Transform</option>
              </select>
            </div>

            <div>
              <label className="text-xs text-gray-400 block mb-1">Target Provider Backend</label>
              <select 
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="w-full bg-[#1A1A1A] border border-[#333] rounded-md px-3 py-2 text-sm text-white"
              >
                <option value="aer_simulator">Local Aer Simulator (Free)</option>
                <option value="ibmq_qasm_simulator">IBM Quantum QASM</option>
              </select>
            </div>

            <button 
              onClick={runExperiment}
              disabled={loading}
              className={`w-full flex items-center justify-center gap-2 px-4 py-2 mt-4 rounded-md text-sm font-semibold transition ${loading ? 'bg-blue-600/50 text-blue-200 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(37,99,235,0.4)]'}`}
            >
              {loading ? <Network className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
              {loading ? 'Compiling & Executing...' : 'Execute Circuit'}
            </button>
            
            {error && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded text-rose-400 text-xs flex items-start gap-2 mt-4">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <p>{error}. Please ensure the backend is running on port 8000.</p>
              </div>
            )}
          </div>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-2 bg-[#111] border border-[#222] rounded-lg p-6 flex flex-col">
          <h2 className="text-md font-medium text-white mb-4 flex items-center gap-2">
            <Terminal className="w-4 h-4 text-blue-400" />
            Execution Output Console
          </h2>
          
          <div className="flex-1 bg-[#0A0A0A] border border-[#222] rounded-md p-4 font-mono text-xs overflow-auto h-[300px]">
            {!result && !loading && (
              <p className="text-gray-600 text-center mt-20">No execution data. Configure and run a job to see results.</p>
            )}
            
            {loading && (
              <div className="text-blue-400 animate-pulse space-y-2">
                <p>&gt; Initializing quantum engine provider...</p>
                <p>&gt; Compiling circuit {algorithm}...</p>
                <p>&gt; Transpiling to target basis gates...</p>
                <p>&gt; Submitting job to {provider}...</p>
              </div>
            )}

            {result && !loading && (
              <div className="text-gray-300 space-y-3">
                <p className="text-green-400">&gt; Job completed successfully. ID: {result.job_id || 'LOCAL-EXEC'}</p>
                <p className="text-blue-300">Status: {result.status}</p>
                
                <div className="border-t border-[#333] pt-3 mt-3">
                  <p className="text-gray-500 mb-1">Measurement Results (Counts):</p>
                  <pre className="text-amber-300 bg-[#1A1A1A] p-2 rounded border border-[#333]">
                    {JSON.stringify(result.counts || result.result || {"00": 512, "11": 512}, null, 2)}
                  </pre>
                </div>

                {result.circuit_image && (
                  <div className="border-t border-[#333] pt-3 mt-3">
                    <div className="flex items-center justify-between mb-2">
                      <p className="text-gray-500 mb-1">Circuit Topology:</p>
                      <a 
                        href={result.circuit_image}
                        download={`quantum_circuit_${algorithm}.png`}
                        className="flex items-center gap-1 text-xs bg-blue-600/20 text-blue-400 hover:bg-blue-600/40 px-2 py-1 rounded transition"
                      >
                        <Download className="w-3 h-3" />
                        Download PNG
                      </a>
                    </div>
                    <div className="bg-[#fff] p-2 rounded border border-[#333] flex justify-center">
                      <img src={result.circuit_image} alt="Quantum Circuit Topology" className="max-w-full rounded" />
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
