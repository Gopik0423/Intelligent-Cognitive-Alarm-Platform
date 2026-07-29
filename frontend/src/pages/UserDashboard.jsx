import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import { Target, Flame, Brain, Clock } from 'lucide-react';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

export default function UserDashboard() {
    const lineOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: { mode: 'index', intersect: false }
        },
        scales: {
            y: { display: false, min: 0, max: 100 },
            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
        },
        elements: {
            line: { tension: 0.4 }
        }
    };

    const lineData = {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [
            {
                fill: true,
                label: 'Habit Score',
                data: [72, 79, 75, 84, 88, 92, 95],
                borderColor: '#a855f7',
                backgroundColor: 'rgba(168, 85, 247, 0.2)',
            },
        ],
    };

    const barData = {
        labels: ['Math', 'Logic', 'Memory', 'Words'],
        datasets: [
            {
                label: 'Accuracy %',
                data: [85, 92, 78, 88],
                backgroundColor: '#3b82f6',
                borderRadius: 4,
            },
        ],
    };

    const barOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
        }
    };

    return (
        <div className="p-8 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold mb-2">Welcome Back, Alex</h1>
                    <p className="text-slate-400">Your sleep structure is improving. Keep it up!</p>
                </div>
                <div className="bg-purple-500/10 px-4 py-2 rounded-xl border border-purple-500/20 text-purple-400 font-semibold shadow-[0_0_15px_rgba(168,85,247,0.15)] flex items-center space-x-2">
                    <Flame className="w-5 h-5 text-orange-400" />
                    <span>12 Day Streak</span>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                    { title: 'Avg Wake Time', value: '06:45 AM', icon: Clock, color: 'text-blue-400', bg: 'bg-blue-400/10' },
                    { title: 'Habit Score', value: '95/100', icon: Target, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
                    { title: 'Challenge Success', value: '92%', icon: Brain, color: 'text-purple-400', bg: 'bg-purple-400/10' },
                    { title: 'Snoozes This Week', value: '2', icon: Clock, color: 'text-rose-400', bg: 'bg-rose-400/10' },
                ].map((kpi, i) => (
                    <div key={i} className="bg-white/5 border border-white/5 p-6 rounded-3xl hover:bg-white/10 transition-colors group">
                        <div className="flex justify-between items-start mb-4">
                            <div className={`p-3 rounded-2xl ${kpi.bg}`}>
                                <kpi.icon className={`w-6 h-6 ${kpi.color}`} />
                            </div>
                        </div>
                        <h3 className="text-slate-400 text-sm mb-1">{kpi.title}</h3>
                        <p className="text-3xl font-bold text-white group-hover:scale-105 transition-transform origin-left">{kpi.value}</p>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Line Chart */}
                <div className="lg:col-span-2 bg-white/5 border border-white/5 p-6 rounded-3xl flex flex-col">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-xl font-bold">Habit Scoring Trend</h2>
                        <select className="bg-black/20 border border-white/10 rounded-lg px-3 py-1 text-sm text-slate-300 focus:outline-none">
                            <option className="bg-slate-900">This Week</option>
                            <option className="bg-slate-900">This Month</option>
                        </select>
                    </div>
                    <div className="flex-1 min-h-[300px]">
                        <Line data={lineData} options={lineOptions} />
                    </div>
                </div>

                {/* Bar Chart */}
                <div className="bg-white/5 border border-white/5 p-6 rounded-3xl flex flex-col">
                    <h2 className="text-xl font-bold mb-6">Challenge Performance</h2>
                    <div className="flex-1 min-h-[300px]">
                        <Bar data={barData} options={barOptions} />
                    </div>
                </div>
            </div>
        </div>
    );
}
