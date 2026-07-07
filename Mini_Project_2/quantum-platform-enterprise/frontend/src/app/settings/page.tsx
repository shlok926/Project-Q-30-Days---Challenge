"use client";

import React, { useState } from 'react';
import { Settings, Shield, Bell, HardDrive, Cpu, Mail, Key } from 'lucide-react';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('provider');

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-semibold text-white mb-1">Platform Settings</h1>
        <p className="text-gray-400 text-sm">Manage configuration, integrations, and preferences.</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        
        {/* Settings Navigation */}
        <div className="col-span-1 space-y-1">
          <button 
            onClick={() => setActiveTab('provider')}
            className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors ${activeTab === 'provider' ? 'bg-[#1A1A1A] text-white border border-[#333]' : 'text-gray-400 hover:text-white hover:bg-[#111] border border-transparent'}`}
          >
            <Cpu className="w-4 h-4" /> Provider APIs
          </button>
          <button 
            onClick={() => setActiveTab('data')}
            className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors ${activeTab === 'data' ? 'bg-[#1A1A1A] text-white border border-[#333]' : 'text-gray-400 hover:text-white hover:bg-[#111] border border-transparent'}`}
          >
            <HardDrive className="w-4 h-4" /> Data Retention
          </button>
          <button 
            onClick={() => setActiveTab('notifications')}
            className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors ${activeTab === 'notifications' ? 'bg-[#1A1A1A] text-white border border-[#333]' : 'text-gray-400 hover:text-white hover:bg-[#111] border border-transparent'}`}
          >
            <Bell className="w-4 h-4" /> Notifications
          </button>
          <button 
            onClick={() => setActiveTab('security')}
            className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors ${activeTab === 'security' ? 'bg-[#1A1A1A] text-white border border-[#333]' : 'text-gray-400 hover:text-white hover:bg-[#111] border border-transparent'}`}
          >
            <Shield className="w-4 h-4" /> Security & Access
          </button>
        </div>

        {/* Settings Content */}
        <div className="col-span-3 space-y-6">
          
          {/* Provider Tab */}
          {activeTab === 'provider' && (
            <div className="bg-[#111] border border-[#222] rounded-lg p-6 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-md font-medium text-white mb-4">Quantum Provider Configuration</h3>
              <div className="space-y-4">
                <div>
                  <label className="text-xs text-gray-400 block mb-1">IBM Quantum API Token</label>
                  <input type="password" value="*************************" disabled className="w-full bg-[#1A1A1A] border border-[#333] rounded-md px-3 py-2 text-sm text-gray-500"/>
                  <p className="text-[10px] text-gray-500 mt-1">Stored securely in HashiCorp Vault. Contact admin to rotate.</p>
                </div>
                <div>
                  <label className="text-xs text-gray-400 block mb-1">Default Execution Target</label>
                  <select className="w-full bg-[#1A1A1A] border border-[#333] rounded-md px-3 py-2 text-sm text-white">
                    <option>Aer Simulator (Local - Free)</option>
                    <option>IBM Quantum (Production QPU)</option>
                    <option>IonQ Aria (Priority Queue)</option>
                  </select>
                </div>
                <div className="flex items-center justify-between pt-2">
                  <span className="text-sm text-gray-300">Enable Auto-Failover to Simulator</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-9 h-5 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>
            </div>
          )}

          {/* Data Retention Tab */}
          {activeTab === 'data' && (
            <div className="bg-[#111] border border-[#222] rounded-lg p-6 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-md font-medium text-white mb-4">Telemetry & Diagnostics</h3>
              <div className="space-y-4">
                <div>
                  <label className="text-xs text-gray-400 block mb-1">Data Retention Period (Days)</label>
                  <input type="number" defaultValue={30} className="w-full bg-[#1A1A1A] border border-[#333] rounded-md px-3 py-2 text-sm text-white"/>
                  <p className="text-[10px] text-gray-500 mt-1">After 30 days, old execution histories are archived to S3 Cold Storage.</p>
                </div>
                <div className="flex items-center justify-between pt-2">
                  <span className="text-sm text-gray-300">Detailed Execution Tracing</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-9 h-5 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
                <div className="flex items-center justify-between pt-2">
                  <span className="text-sm text-gray-300">Export Raw Measurement Counts</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" />
                    <div className="w-9 h-5 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>
            </div>
          )}

          {/* Notifications Tab */}
          {activeTab === 'notifications' && (
            <div className="bg-[#111] border border-[#222] rounded-lg p-6 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-md font-medium text-white mb-4">Alerts & Notifications</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between border-b border-[#222] pb-4">
                  <div className="flex items-center gap-3">
                    <Mail className="w-5 h-5 text-gray-400" />
                    <div>
                      <p className="text-sm text-gray-300">Email Alerts on Failure</p>
                      <p className="text-[10px] text-gray-500">Receive emails when a QPU job crashes.</p>
                    </div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" defaultChecked />
                    <div className="w-9 h-5 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Network className="w-5 h-5 text-gray-400" />
                    <div>
                      <p className="text-sm text-gray-300">Slack Webhook URL</p>
                      <p className="text-[10px] text-gray-500">Send notifications directly to a Slack channel.</p>
                    </div>
                  </div>
                  <input type="text" placeholder="https://hooks.slack.com/..." className="w-48 bg-[#1A1A1A] border border-[#333] rounded-md px-3 py-1.5 text-xs text-white"/>
                </div>
              </div>
            </div>
          )}

          {/* Security Tab */}
          {activeTab === 'security' && (
            <div className="bg-[#111] border border-[#222] rounded-lg p-6 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-md font-medium text-white mb-4">Security & Access Control</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between border-b border-[#222] pb-4">
                  <div className="flex items-center gap-3">
                    <Shield className="w-5 h-5 text-gray-400" />
                    <div>
                      <p className="text-sm text-gray-300">Two-Factor Authentication (2FA)</p>
                      <p className="text-[10px] text-gray-500">Require an authenticator app for login.</p>
                    </div>
                  </div>
                  <button className="px-3 py-1.5 bg-[#1A1A1A] border border-[#333] text-gray-300 text-xs rounded hover:bg-[#222]">
                    Enable 2FA
                  </button>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Key className="w-5 h-5 text-gray-400" />
                    <div>
                      <p className="text-sm text-gray-300">Personal Access Tokens</p>
                      <p className="text-[10px] text-gray-500">Generate tokens for CLI and REST API access.</p>
                    </div>
                  </div>
                  <button className="px-3 py-1.5 bg-white text-black font-semibold text-xs rounded hover:bg-gray-200">
                    Generate New
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Save Button */}
          <div className="flex justify-end gap-3 pt-4 border-t border-[#222]">
            <button className="px-4 py-2 bg-[#1A1A1A] text-gray-300 rounded-md text-sm font-medium hover:bg-[#222] transition-colors border border-[#333]">
              Cancel
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-500 shadow-[0_0_15px_rgba(37,99,235,0.2)] transition-colors">
              Save Changes
            </button>
          </div>
          
        </div>
      </div>
    </div>
  );
}
