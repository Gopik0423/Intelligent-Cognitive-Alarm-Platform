import React, { useState } from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, RadarChart, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import { Download, Activity, Moon, Clock, Target, Award, Calendar, BarChart2 } from 'lucide-react';

const sleepData = [
  { date: 'Mon', hours: 6.5, deepSleep: 2 },
  { date: 'Tue', hours: 7.2, deepSleep: 2.5 },
  { date: 'Wed', hours: 6.8, deepSleep: 2.1 },
  { date: 'Thu', hours: 7.5, deepSleep: 3 },
  { date: 'Fri', hours: 8.1, deepSleep: 3.5 },
  { date: 'Sat', hours: 8.5, deepSleep: 4 },
  { date: 'Sun', hours: 7.8, deepSleep: 3.2 },
];

const wakeupTrends = [
  { date: 'Mon', time: 6.5 },
  { date: 'Tue', time: 6.2 },
  { date: 'Wed', time: 6.3 },
  { date: 'Thu', time: 6.0 },
  { date: 'Fri', time: 5.8 },
  { date: 'Sat', time: 7.5 },
  { date: 'Sun', time: 7.0 },
];

const snoozeBehavior = [
  { name: '0 Snoozes', value: 45, color: '#10b981' },
  { name: '1 Snooze', value: 30, color: '#6366f1' },
  { name: '2 Snoozes', value: 15, color: '#f59e0b' },
  { name: '3+ Snoozes', value: 10, color: '#ef4444' },
];

const challengePerformance = [
  { subject: 'Math', A: 85, fullMark: 100 },
  { subject: 'Memory', A: 92, fullMark: 100 },
  { subject: 'Puzzle', A: 78, fullMark: 100 },
  { subject: 'Typing', A: 88, fullMark: 100 },
  { subject: 'Logic', A: 95, fullMark: 100 },
];

const habitScores = [
  { week: 'Week 1', score: 75 },
  { week: 'Week 2', score: 82 },
  { week: 'Week 3', score: 88 },
  { week: 'Week 4', score: 94 },
];

function CustomTooltip({ active, payload, label }) {
  if (active && payload && payload.length) {
    return (
      <div style={{ background: 'rgba(15, 17, 26, 0.9)', border: '1px solid rgba(255, 255, 255, 0.1)', padding: '12px', borderRadius: '8px', backdropFilter: 'blur(8px)' }}>
        <p style={{ margin: 0, color: '#f8fafc', fontWeight: 600, marginBottom: '8px' }}>{label}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ margin: 0, color: entry.color || '#a5b4fc', fontSize: '13px' }}>
            {entry.name}: {entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
}

function App() {
  const [filter, setFilter] = useState('week');

  const generateReport = () => {
    alert(`Generating performance report for Current ${filter}...`);
  };

  return (
    <div className="dashboard-container">
      <header className="header-row">
        <div>
          <h1>Performance & Visualization</h1>
          <p className="subtitle">Monitor your cognitive alarm stats and sleep health</p>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '16px' }}>
          <div className="filter-group">
            {['day', 'week', 'month'].map((f) => (
              <button
                key={f}
                className={`filter-btn ${filter === f ? 'active' : ''}`}
                onClick={() => setFilter(f)}
              >
                {f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}
          </div>
          <button className="btn-primary" onClick={generateReport}>
            <Download size={18} />
            Generate Report
          </button>
        </div>
      </header>

      <div className="grid-layout">
        
        {/* KPIs row */}
        <div className="col-span-12 grid-layout" style={{ gap: '24px', gridTemplateColumns: 'repeat(4, 1fr)' }}>
          <div className="glass-panel kpi-card" style={{ gridColumn: 'span 1' }}>
            <div className="kpi-label">Avg Sleep Duration</div>
            <div className="kpi-value">7.2h</div>
            <div className="kpi-trend positive">+0.4h from last week</div>
          </div>
          <div className="glass-panel kpi-card" style={{ gridColumn: 'span 1' }}>
            <div className="kpi-label">Avg Wake Time</div>
            <div className="kpi-value">6:30 AM</div>
            <div className="kpi-trend positive">-15m (earlier)</div>
          </div>
          <div className="glass-panel kpi-card" style={{ gridColumn: 'span 1' }}>
            <div className="kpi-label">Snooze Resistance</div>
            <div className="kpi-value">75%</div>
            <div className="kpi-trend negative">-2% from last week</div>
          </div>
          <div className="glass-panel kpi-card" style={{ gridColumn: 'span 1' }}>
            <div className="kpi-label">Habit Score</div>
            <div className="kpi-value">94</div>
            <div className="kpi-trend positive">+6 points</div>
          </div>
        </div>

        {/* Chart 1: Sleep Patterns */}
        <div className="col-span-8 glass-panel">
          <h3 className="chart-title"><Moon size={20} /> Sleep Patterns & Deep Sleep</h3>
          <div style={{ width: '100%', height: 320 }}>
            <ResponsiveContainer>
              <AreaChart data={sleepData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorHours" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorDeep" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid vertical={false} />
                <XAxis dataKey="date" axisLine={false} tickLine={false} />
                <YAxis axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="hours" name="Total Sleep" stroke="#6366f1" strokeWidth={3} fillOpacity={1} fill="url(#colorHours)" />
                <Area type="monotone" dataKey="deepSleep" name="Deep Sleep" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorDeep)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Snooze Behavior */}
        <div className="col-span-4 glass-panel">
          <h3 className="chart-title"><Clock size={20} /> Snooze Behavior</h3>
          <div style={{ width: '100%', height: 320 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={snoozeBehavior}
                  innerRadius={80}
                  outerRadius={110}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {snoozeBehavior.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(15, 17, 26, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                  itemStyle={{ color: '#fff' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', justifyContent: 'center', marginTop: '16px' }}>
            {snoozeBehavior.map((item, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: item.color }} />
                {item.name} ({item.value}%)
              </div>
            ))}
          </div>
        </div>

        {/* Chart 3: Wake-up Trends */}
        <div className="col-span-6 glass-panel">
          <h3 className="chart-title"><Activity size={20} /> Wake-up Time Trends</h3>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <LineChart data={wakeupTrends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid vertical={false} />
                <XAxis dataKey="date" axisLine={false} tickLine={false} />
                <YAxis axisLine={false} tickLine={false} domain={[5, 9]} tickFormatter={(val) => `${val}:00`} />
                <Tooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="time" name="Wake Time" stroke="#f59e0b" strokeWidth={4} dot={{ r: 4, fill: '#f59e0b', strokeWidth: 2, stroke: '#0f111a' }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 4: Challenge Performance */}
        <div className="col-span-6 glass-panel">
          <h3 className="chart-title"><Target size={20} /> Challenge Performance</h3>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={challengePerformance}>
                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar name="Score" dataKey="A" stroke="#8b5cf6" strokeWidth={3} fill="#8b5cf6" fillOpacity={0.5} />
                <Tooltip content={<CustomTooltip />} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 5: Habit Score Visualization */}
        <div className="col-span-12 glass-panel">
          <h3 className="chart-title"><Award size={20} /> Habit Score Progression</h3>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <BarChart data={habitScores} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid vertical={false} />
                <XAxis dataKey="week" axisLine={false} tickLine={false} />
                <YAxis axisLine={false} tickLine={false} domain={[0, 100]} />
                <Tooltip cursor={{ fill: 'rgba(255,255,255,0.05)' }} content={<CustomTooltip />} />
                <Bar dataKey="score" name="Habit Score" fill="#10b981" radius={[6, 6, 0, 0]} maxBarSize={60} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
