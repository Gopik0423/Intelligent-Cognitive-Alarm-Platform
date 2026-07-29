import React from 'react';
import { Users, TrendingUp, AlertTriangle, FileText } from 'lucide-react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function WellnessDashboard() {
    const doughdata = {
        labels: ['Consistent', 'Struggling', 'At Risk'],
        datasets: [
            {
                data: [65, 25, 10],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)', // emerald
                    'rgba(245, 158, 11, 0.8)', // amber
                    'rgba(239, 68, 68, 0.8)', // rose
                ],
                borderWidth: 0,
            },
        ],
    };

    return (
        <div className="p-8 space-y-8">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">Coach Portal</h1>
                    <p className="text-slate-400 mt-2">Monitor client sleep patterns and habit adherence.</p>
                </div>
                <button className="bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 px-4 py-2 rounded-xl flex items-center space-x-2 border border-emerald-500/20 transition-all">
                    <FileText className="w-4 h-4" />
                    <span>Export All Reports</span>
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-emerald-500/10 border border-emerald-500/20 p-6 rounded-3xl">
                    <div className="flex items-center space-x-4 mb-4">
                        <div className="p-3 bg-emerald-500/20 rounded-xl text-emerald-400"><Users /></div>
                        <h3 className="text-lg font-semibold text-emerald-100">Total Clients</h3>
                    </div>
                    <p className="text-4xl font-bold text-white">124</p>
                </div>
                <div className="bg-blue-500/10 border border-blue-500/20 p-6 rounded-3xl">
                    <div className="flex items-center space-x-4 mb-4">
                        <div className="p-3 bg-blue-500/20 rounded-xl text-blue-400"><TrendingUp /></div>
                        <h3 className="text-lg font-semibold text-blue-100">Avg Habit Score</h3>
                    </div>
                    <p className="text-4xl font-bold text-white">82</p>
                </div>
                <div className="bg-rose-500/10 border border-rose-500/20 p-6 rounded-3xl">
                    <div className="flex items-center space-x-4 mb-4">
                        <div className="p-3 bg-rose-500/20 rounded-xl text-rose-400"><AlertTriangle /></div>
                        <h3 className="text-lg font-semibold text-rose-100">Needs Attention</h3>
                    </div>
                    <p className="text-4xl font-bold text-white">12</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="bg-white/5 border border-white/5 p-6 rounded-3xl col-span-1 flex flex-col items-center">
                    <h2 className="text-xl font-bold self-start w-full mb-4">Client Adherence</h2>
                    <div className="w-64 h-64">
                        <Doughnut data={doughdata} options={{ maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } } }} />
                    </div>
                </div>

                <div className="bg-white/5 border border-white/5 rounded-3xl col-span-2 overflow-hidden flex flex-col">
                    <div className="p-6 border-b border-white/5 flex justify-between items-center">
                        <h2 className="text-xl font-bold">Client Roster</h2>
                        <input type="text" placeholder="Search clients..." className="bg-black/20 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-emerald-500" />
                    </div>
                    <div className="flex-1 overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="text-slate-400 text-sm bg-black/10">
                                    <th className="p-4 font-medium">Name</th>
                                    <th className="p-4 font-medium">Habit Score</th>
                                    <th className="p-4 font-medium">Snooze Rate</th>
                                    <th className="p-4 font-medium">Trend</th>
                                    <th className="p-4 font-medium">Action</th>
                                </tr>
                            </thead>
                            <tbody className="text-sm divide-y divide-white/5">
                                {[
                                    { name: 'Sarah Jenkins', score: 92, snooze: '5%', trend: 'up' },
                                    { name: 'Mike Ross', score: 78, snooze: '15%', trend: 'up' },
                                    { name: 'Emily Clarke', score: 45, snooze: '42%', trend: 'down' },
                                    { name: 'David Lee', score: 88, snooze: '8%', trend: 'up' },
                                ].map((client, i) => (
                                    <tr key={i} className="hover:bg-white/5 transition-colors">
                                        <td className="p-4 text-white font-medium">{client.name}</td>
                                        <td className="p-4">
                                            <div className="flex items-center space-x-2">
                                                <div className="w-full bg-slate-800 rounded-full h-2 max-w-[100px]">
                                                    <div className={`h-2 rounded-full ${client.score > 80 ? 'bg-emerald-500' : client.score > 60 ? 'bg-amber-500' : 'bg-rose-500'}`} style={{ width: `${client.score}%` }}></div>
                                                </div>
                                                <span className="text-slate-300">{client.score}</span>
                                            </div>
                                        </td>
                                        <td className="p-4 text-slate-300">{client.snooze}</td>
                                        <td className="p-4">
                                            {client.trend === 'up' ? <TrendingUp className="w-4 h-4 text-emerald-500" /> : <TrendingUp className="w-4 h-4 text-rose-500 rotate-180" />}
                                        </td>
                                        <td className="p-4">
                                            <button className="text-emerald-400 hover:text-emerald-300 font-medium">View Profile</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}
