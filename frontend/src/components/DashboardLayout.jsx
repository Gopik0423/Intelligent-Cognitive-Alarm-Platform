import React from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, AlarmClock, Activity, Settings, Bell, LogOut, ShieldAlert } from 'lucide-react';

export default function DashboardLayout() {
    const navigate = useNavigate();

    const navItems = [
        { name: 'My Dashboard', path: '/dashboard', icon: LayoutDashboard, exact: true },
        { name: 'Alarms', path: '/dashboard/alarms', icon: AlarmClock },
        { name: 'Coach View', path: '/dashboard/coach', icon: Activity },
        { name: 'Admin', path: '/dashboard/admin', icon: ShieldAlert },
        { name: 'Notifications', path: '/dashboard/notifications', icon: Bell },
    ];

    return (
        <div className="flex h-screen bg-slate-950 text-white overflow-hidden">
            {/* Sidebar */}
            <aside className="w-72 border-r border-white/10 bg-slate-950/50 backdrop-blur-xl flex flex-col z-20 shadow-2xl relative">
                <div className="p-6 flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-tr from-purple-500 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/20">
                        <Settings className="w-5 h-5" />
                    </div>
                    <h1 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                        Cognitive Alarm
                    </h1>
                </div>

                <nav className="flex-1 px-4 space-y-2 mt-4 overflow-y-auto">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.name}
                            to={item.path}
                            end={item.exact}
                            className={({ isActive }) =>
                                `flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${isActive
                                    ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20 shadow-lg shadow-purple-500/5'
                                    : 'text-slate-400 hover:bg-white/5 hover:text-white'
                                }`
                            }
                        >
                            <item.icon className="w-5 h-5 flex-shrink-0" />
                            <span className="font-medium">{item.name}</span>
                        </NavLink>
                    ))}
                </nav>

                <div className="p-4 border-t border-white/10">
                    <button
                        onClick={() => navigate('/auth')}
                        className="flex items-center space-x-3 px-4 py-3 w-full rounded-xl text-slate-400 hover:bg-white/5 hover:text-rose-400 transition-colors"
                    >
                        <LogOut className="w-5 h-5" />
                        <span className="font-medium">Sign Out</span>
                    </button>
                </div>
            </aside>

            {/* Main Content Area */}
            <main className="flex-1 relative overflow-hidden flex flex-col bg-[#0f111a]">
                {/* Ambient background light */}
                <div className="absolute top-[-20%] left-[20%] w-[50rem] h-[50rem] bg-indigo-500/5 rounded-full blur-[120px] pointer-events-none mix-blend-screen"></div>

                <div className="flex-1 overflow-y-auto z-10 scrollbar-thin scrollbar-thumb-purple-900 scrollbar-track-transparent">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
