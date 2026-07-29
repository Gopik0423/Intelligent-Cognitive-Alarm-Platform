import React, { useState } from 'react';
import { Bell, Smartphone, Mail, Moon, Trophy, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function NotificationSettings() {
    const [activeTab, setActiveTab] = useState('settings');

    const notifications = [
        { id: 1, title: 'Habit Goal Reached!', desc: 'You woke up on time 5 days in a row.', time: '2 hours ago', icon: Trophy, color: 'text-yellow-400', unread: true },
        { id: 2, title: 'Bedtime Reminder', desc: 'Your optimal bedtime is in 30 minutes.', time: 'Yesterday', icon: Moon, color: 'text-indigo-400', unread: false },
        { id: 3, title: 'Alarm Missed', desc: 'You snoozed through your 7:00 AM alarm.', time: '2 days ago', icon: AlertCircle, color: 'text-rose-400', unread: false },
    ];

    return (
        <div className="p-8 max-w-4xl mx-auto space-y-8">
            <div>
                <h1 className="text-3xl font-bold mb-2">Notifications</h1>
                <p className="text-slate-400">Manage your alerts and view recent activity.</p>
            </div>

            <div className="flex space-x-1 bg-black/20 p-1 rounded-xl w-fit border border-white/5">
                <button
                    onClick={() => setActiveTab('settings')}
                    className={`px-6 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'settings' ? 'bg-white/10 text-white shadow-lg' : 'text-slate-400 hover:text-white'
                        }`}
                >
                    Preferences
                </button>
                <button
                    onClick={() => setActiveTab('inbox')}
                    className={`px-6 py-2 rounded-lg text-sm font-medium transition-all flex items-center space-x-2 ${activeTab === 'inbox' ? 'bg-white/10 text-white shadow-lg' : 'text-slate-400 hover:text-white'
                        }`}
                >
                    <span>Inbox</span>
                    <span className="w-2 h-2 rounded-full bg-purple-500"></span>
                </button>
            </div>

            {activeTab === 'settings' && (
                <div className="space-y-6 animate-in fade-in duration-300">
                    <div className="bg-white/5 border border-white/5 rounded-3xl overflow-hidden">
                        <div className="p-6 border-b border-white/5 flex items-center space-x-3">
                            <Smartphone className="w-5 h-5 text-purple-400" />
                            <h2 className="text-xl font-bold">Push Notifications</h2>
                        </div>
                        <div className="p-6 space-y-6">
                            {[
                                { label: 'Bedtime Reminders', desc: 'Alerts 30 mins before optimal sleep time' },
                                { label: 'Wake-Up Summary', desc: 'Morning performance after dismissing alarms' },
                                { label: 'Challenge Adjustments', desc: 'When AI adapts your puzzle difficulty' },
                                { label: 'Habit Milestones', desc: 'Celebrations for consistent streaks' },
                            ].map((setting, i) => (
                                <div key={i} className="flex justify-between items-center group">
                                    <div>
                                        <h3 className="font-medium text-slate-200">{setting.label}</h3>
                                        <p className="text-sm text-slate-400">{setting.desc}</p>
                                    </div>
                                    <label className="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" className="sr-only peer" defaultChecked={i !== 2} />
                                        <div className="w-11 h-6 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-500"></div>
                                    </label>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="bg-white/5 border border-white/5 rounded-3xl overflow-hidden">
                        <div className="p-6 border-b border-white/5 flex items-center space-x-3">
                            <Mail className="w-5 h-5 text-blue-400" />
                            <h2 className="text-xl font-bold">Email Notifications</h2>
                        </div>
                        <div className="p-6 space-y-6">
                            {[
                                { label: 'Weekly Habit Reports', desc: 'Detailed analytics of your sleep patterns' },
                                { label: 'Coach Messages', desc: 'Direct feedback from your wellness coach' },
                                { label: 'Platform Updates', desc: 'New puzzle types and features' },
                            ].map((setting, i) => (
                                <div key={i} className="flex justify-between items-center group">
                                    <div>
                                        <h3 className="font-medium text-slate-200">{setting.label}</h3>
                                        <p className="text-sm text-slate-400">{setting.desc}</p>
                                    </div>
                                    <label className="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" className="sr-only peer" defaultChecked={i === 0} />
                                        <div className="w-11 h-6 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-500"></div>
                                    </label>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {activeTab === 'inbox' && (
                <div className="bg-white/5 border border-white/5 rounded-3xl overflow-hidden animate-in fade-in duration-300">
                    <div className="p-4 border-b border-white/5 flex justify-between items-center bg-black/10">
                        <h2 className="font-semibold px-2">Recent Activity</h2>
                        <button className="text-sm text-purple-400 hover:text-purple-300 flex items-center space-x-1 px-3 py-1.5 rounded-lg hover:bg-purple-500/10 transition-colors">
                            <CheckCircle2 className="w-4 h-4" />
                            <span>Mark all read</span>
                        </button>
                    </div>
                    <div className="divide-y divide-white/5">
                        {notifications.map((notif) => (
                            <div key={notif.id} className={`p-6 flex gap-4 hover:bg-white/5 transition-colors ${notif.unread ? 'bg-white/[0.02]' : ''}`}>
                                <div className={`p-3 rounded-xl h-fit ${notif.unread ? 'bg-white/10' : 'bg-black/20'}`}>
                                    <notif.icon className={`w-6 h-6 ${notif.color}`} />
                                </div>
                                <div className="flex-1">
                                    <div className="flex justify-between items-start mb-1">
                                        <h3 className={`font-semibold ${notif.unread ? 'text-white text-base' : 'text-slate-300 text-sm'}`}>
                                            {notif.title}
                                        </h3>
                                        <span className="text-xs text-slate-500">{notif.time}</span>
                                    </div>
                                    <p className={`text-sm ${notif.unread ? 'text-slate-300' : 'text-slate-500'}`}>
                                        {notif.desc}
                                    </p>
                                </div>
                                {notif.unread && (
                                    <div className="flex items-center justify-center">
                                        <div className="w-2.5 h-2.5 rounded-full bg-purple-500 shadow-[0_0_8px_rgba(168,85,247,0.8)]"></div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
