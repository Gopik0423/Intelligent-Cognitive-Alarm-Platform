import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Moon, Sun, Target, BrainCircuit, ArrowRight } from 'lucide-react';

export default function ProfileCreation() {
    const navigate = useNavigate();
    const [step, setStep] = useState(1);

    return (
        <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4 relative overflow-hidden text-white">
            <div className="absolute top-0 right-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute top-[-10%] right-[-5%] w-[40rem] h-[40rem] bg-indigo-600/20 rounded-full blur-[120px] mix-blend-screen"></div>
                <div className="absolute bottom-[-10%] left-[-5%] w-[40rem] h-[40rem] bg-rose-600/20 rounded-full blur-[120px] mix-blend-screen"></div>
            </div>

            <div className="w-full max-w-2xl bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl z-10">
                <div className="flex justify-between items-center mb-8">
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="flex items-center">
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-500
                ${step >= i ? 'border-purple-500 bg-purple-500/20 text-purple-400' : 'border-slate-700 text-slate-500'}`}>
                                {i}
                            </div>
                            {i < 3 && (
                                <div className={`w-24 h-1 mx-2 rounded transition-all duration-500 ${step > i ? 'bg-purple-500/50' : 'bg-slate-800'}`} />
                            )}
                        </div>
                    ))}
                </div>

                {step === 1 && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
                        <div className="text-center">
                            <Moon className="w-12 h-12 text-purple-400 mx-auto mb-4" />
                            <h2 className="text-2xl font-bold mb-2">Sleep Preferences</h2>
                            <p className="text-slate-400">Tell us about your sleep habits to customize your experience.</p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <label className="text-sm text-slate-300">Target Sleep Duration</label>
                                <select className="w-full bg-black/20 border border-white/10 rounded-xl py-3 px-4 text-white hover:border-purple-500 transition-colors focus:outline-none focus:ring-1 focus:ring-purple-500">
                                    <option className="bg-slate-900">6 hours (Not recommended)</option>
                                    <option className="bg-slate-900">7 hours</option>
                                    <option className="bg-slate-900" selected>8 hours (Optimal)</option>
                                    <option className="bg-slate-900">9 hours</option>
                                </select>
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm text-slate-300">Ideal Wake Time</label>
                                <input type="time" defaultValue="07:00" className="w-full bg-black/20 border border-white/10 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-purple-500 transition-all [&::-webkit-calendar-picker-indicator]:filter-[invert(1)]" />
                            </div>
                        </div>
                    </div>
                )}

                {step === 2 && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
                        <div className="text-center">
                            <Target className="w-12 h-12 text-blue-400 mx-auto mb-4" />
                            <h2 className="text-2xl font-bold mb-2">Habit Goals</h2>
                            <p className="text-slate-400">What are you hoping to achieve?</p>
                        </div>

                        <div className="grid grid-cols-1 gap-3">
                            {['Stop Snoozing Completely', 'Establish Morning Routine', 'Improve Sleep Quality', 'Boost Morning Productivity'].map((goal) => (
                                <label key={goal} className="flex items-center space-x-3 p-4 rounded-xl border border-white/10 bg-black/10 hover:bg-white/5 cursor-pointer transition-colors group">
                                    <input type="checkbox" className="w-5 h-5 rounded border-slate-600 text-purple-500 focus:ring-purple-500/20 bg-slate-800" />
                                    <span className="text-slate-200 group-hover:text-white transition-colors">{goal}</span>
                                </label>
                            ))}
                        </div>
                    </div>
                )}

                {step === 3 && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
                        <div className="text-center">
                            <BrainCircuit className="w-12 h-12 text-emerald-400 mx-auto mb-4" />
                            <h2 className="text-2xl font-bold mb-2">Cognitive Challenge Setup</h2>
                            <p className="text-slate-400">Select your preferred wake-up puzzles.</p>
                        </div>

                        <div className="space-y-4">
                            <div>
                                <label className="text-sm text-slate-300 mb-2 block">Starting Difficulty</label>
                                <input type="range" min="1" max="5" defaultValue="2" className="w-full accent-purple-500" />
                                <div className="flex justify-between text-xs text-slate-400 mt-2">
                                    <span>Beginner</span>
                                    <span>Expert</span>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-3 mt-4">
                                {['Math Problems', 'Logic Puzzles', 'Memory Games', 'Pattern Recognition'].map((type) => (
                                    <label key={type} className="flex items-center space-x-2 p-3 rounded-lg border border-white/5 bg-black/20 hover:bg-white/5 cursor-pointer transition-colors">
                                        <input type="checkbox" defaultChecked className="rounded text-purple-500" />
                                        <span className="text-sm text-slate-300">{type}</span>
                                    </label>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                <div className="mt-8 flex justify-between">
                    <button
                        onClick={() => step > 1 ? setStep(step - 1) : navigate('/auth')}
                        className="px-6 py-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
                    >
                        {step === 1 ? 'Cancel' : 'Back'}
                    </button>

                    <button
                        onClick={() => step < 3 ? setStep(step + 1) : navigate('/dashboard')}
                        className="px-6 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium transition-all shadow-lg hover:shadow-purple-500/25 flex items-center space-x-2"
                    >
                        <span>{step === 3 ? 'Complete Setup' : 'Continue'}</span>
                        {step !== 3 && <ArrowRight className="w-4 h-4" />}
                    </button>
                </div>
            </div>
        </div>
    );
}
