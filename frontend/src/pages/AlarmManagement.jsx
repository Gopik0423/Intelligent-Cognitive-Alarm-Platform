import React, { useState } from 'react';
import { Plus, Clock, BrainCircuit, GripVertical, Trash2, Edit2, Play } from 'lucide-react';

export default function AlarmManagement() {
    const [alarms, setAlarms] = useState([
        { id: 1, time: '06:30', ampm: 'AM', label: 'Morning Deep Work', days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], active: true, diff: 'Hard', puzzle: 'Math' },
        { id: 2, time: '08:00', ampm: 'AM', label: 'Weekend Run', days: ['Sat', 'Sun'], active: false, diff: 'Medium', puzzle: 'Logic' },
    ]);

    const toggleAlarm = (id) => {
        setAlarms(alarms.map(a => a.id === id ? { ...a, active: !a.active } : a));
    };

    return (
        <div className="p-8 max-w-5xl mx-auto space-y-8 relative">
            <div className="flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold mb-2">My Alarms</h1>
                    <p className="text-slate-400">Manage your cognitive wake-up schedule.</p>
                </div>
                <button className="bg-purple-600 hover:bg-purple-500 text-white px-5 py-2.5 rounded-xl flex items-center space-x-2 transition-all shadow-lg shadow-purple-500/25 active:scale-95">
                    <Plus className="w-5 h-5" />
                    <span className="font-medium">New Alarm</span>
                </button>
            </div>

            <div className="grid gap-4">
                {alarms.map((alarm) => (
                    <div key={alarm.id} className={`group relative p-6 rounded-3xl border transition-all duration-300 ${alarm.active
                            ? 'bg-white/5 border-purple-500/30 shadow-[0_0_30px_rgba(168,85,247,0.05)]'
                            : 'bg-black/20 border-white/5 opacity-75'
                        }`}>
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">

                            <div className="flex items-center space-x-6">
                                <div className="hidden md:flex text-slate-600 cursor-grab opacity-0 group-hover:opacity-100 transition-opacity">
                                    <GripVertical className="w-5 h-5" />
                                </div>
                                <div>
                                    <div className="flex items-baseline space-x-2">
                                        <span className={`text-5xl font-light tabular-nums tracking-tighter ${alarm.active ? 'text-white' : 'text-slate-400'}`}>
                                            {alarm.time}
                                        </span>
                                        <span className={`text-xl font-medium ${alarm.active ? 'text-purple-400' : 'text-slate-500'}`}>
                                            {alarm.ampm}
                                        </span>
                                    </div>
                                    <h3 className={`mt-1 font-medium ${alarm.active ? 'text-slate-200' : 'text-slate-500'}`}>{alarm.label}</h3>
                                </div>
                            </div>

                            <div className="flex-1 flex flex-col md:items-center space-y-3 px-4">
                                <div className="flex space-x-1">
                                    {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day) => (
                                        <span key={day} className={`text-xs font-semibold w-8 h-8 flex items-center justify-center rounded-full transition-colors ${alarm.days.includes(day)
                                                ? (alarm.active ? 'bg-purple-500/20 text-purple-400' : 'bg-white/10 text-slate-300')
                                                : 'text-slate-600 bg-transparent'
                                            }`}>
                                            {day[0]}
                                        </span>
                                    ))}
                                </div>
                                <div className="flex space-x-3 text-xs">
                                    <span className={`flex items-center space-x-1 px-2.5 py-1 rounded-lg ${alarm.active ? 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/20' : 'text-slate-500 border border-white/5'}`}>
                                        <BrainCircuit className="w-3 h-3" />
                                        <span>{alarm.puzzle}</span>
                                    </span>
                                    <span className={`flex items-center space-x-1 px-2.5 py-1 rounded-lg ${alarm.active ? 'bg-rose-500/10 text-rose-300 border border-rose-500/20' : 'text-slate-500 border border-white/5'}`}>
                                        <span>Lvl: {alarm.diff}</span>
                                    </span>
                                </div>
                            </div>

                            <div className="flex items-center space-x-6 justify-between md:justify-end">
                                <div className="flex space-x-2">
                                    <button className="p-2 rounded-xl text-slate-400 hover:bg-white/10 hover:text-white transition-colors" title="Test Alarm">
                                        <Play className="w-5 h-5 fill-current" />
                                    </button>
                                    <button className="p-2 rounded-xl text-slate-400 hover:bg-white/10 hover:text-white transition-colors">
                                        <Edit2 className="w-5 h-5" />
                                    </button>
                                    <button className="p-2 rounded-xl text-slate-400 hover:bg-rose-500/20 hover:text-rose-400 transition-colors">
                                        <Trash2 className="w-5 h-5" />
                                    </button>
                                </div>

                                {/* Custom Toggle Switch */}
                                <label className="relative inline-flex items-center cursor-pointer">
                                    <input type="checkbox" className="sr-only peer" checked={alarm.active} onChange={() => toggleAlarm(alarm.id)} />
                                    <div className="w-14 h-7 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-purple-500"></div>
                                </label>
                            </div>

                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
