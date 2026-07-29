import React from 'react';
import { Server, Activity, Users, ShieldAlert, Cpu } from 'lucide-react';

export default function AdminDashboard() {
    return (
        <div className="p-8 space-y-8">
            <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">System Admin</h1>
                <p className="text-slate-400 mt-2">Platform analytics and system health.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                    { title: 'Total Users', value: '12.4K', icon: Users, color: 'text-blue-400', bg: 'bg-blue-400/10' },
                    { title: 'API Uptime', value: '99.98%', icon: Server, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
                    { title: 'Server Load', value: '42%', icon: Cpu, color: 'text-amber-400', bg: 'bg-amber-400/10' },
                    { title: 'Active Alarms', value: '8.2K', icon: Activity, color: 'text-purple-400', bg: 'bg-purple-400/10' },
                ].map((kpi, i) => (
                    <div key={i} className="bg-white/5 border border-white/5 p-6 rounded-3xl flex items-center space-x-4">
                        <div className={`p-4 rounded-xl ${kpi.bg}`}>
                            <kpi.icon className={`w-8 h-8 ${kpi.color}`} />
                        </div>
                        <div>
                            <p className="text-slate-400 text-sm font-medium">{kpi.title}</p>
                            <h3 className="text-2xl font-bold text-white">{kpi.value}</h3>
                        </div>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white/5 border border-white/5 p-6 rounded-3xl">
                    <h2 className="text-xl font-bold mb-4 flex items-center space-x-2">
                        <ShieldAlert className="w-5 h-5 text-rose-400" />
                        <span>Recent System Alerts</span>
                    </h2>
                    <div className="space-y-4">
                        {[
                            { time: '10 mins ago', msg: 'High CPU usage detected on Node 4', type: 'warning' },
                            { time: '2 hours ago', msg: 'Database backup completed successfully', type: 'success' },
                            { time: '5 hours ago', msg: 'Failed login spikes detected from IP 192.168.x.x', type: 'error' },
                        ].map((alert, i) => (
                            <div key={i} className="p-4 rounded-xl bg-black/20 border border-white/5 flex justify-between items-start">
                                <div className="flex items-center space-x-3">
                                    <div className={`w-2 h-2 rounded-full ${alert.type === 'error' ? 'bg-rose-500' : alert.type === 'warning' ? 'bg-amber-500' : 'bg-emerald-500'
                                        }`} />
                                    <p className="text-sm text-slate-300">{alert.msg}</p>
                                </div>
                                <span className="text-xs text-slate-500">{alert.time}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-white/5 border border-white/5 p-6 rounded-3xl">
                    <h2 className="text-xl font-bold mb-4">Challenge Engine Status</h2>
                    <div className="space-y-6 mt-6">
                        {[
                            { name: 'Challenge Generator service', status: 'Healthy', load: 35 },
                            { name: 'Analytics Processing', status: 'Healthy', load: 62 },
                            { name: 'Authentication Auth0/JWT', status: 'Healthy', load: 15 },
                        ].map((service, i) => (
                            <div key={i} className="space-y-2">
                                <div className="flex justify-between items-center text-sm">
                                    <span className="text-slate-300 font-medium">{service.name}</span>
                                    <span className="text-emerald-400 bg-emerald-400/10 px-2 py-0.5 rounded-full text-xs border border-emerald-400/20">{service.status}</span>
                                </div>
                                <div className="w-full bg-slate-800 rounded-full h-1.5">
                                    <div className={`h-1.5 rounded-full ${service.load > 60 ? 'bg-amber-500' : 'bg-indigo-500'}`} style={{ width: `${service.load}%` }}></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
