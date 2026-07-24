import React, { useState, useEffect, useRef } from 'react';

// API Base URL - fallback to localhost in dev
const API_BASE = 'http://localhost:8000';

function App() {
  // Authentication states
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [role, setRole] = useState(localStorage.getItem('role') || 'user');
  const [email, setEmail] = useState(localStorage.getItem('email') || '');
  const [password, setPassword] = useState('');
  const [authError, setAuthError] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);

  // Layout and Navigation
  const [activeTab, setActiveTab] = useState('dashboard');

  // App States
  const [profile, setProfile] = useState({
    preferred_wake_up_time: '07:00',
    sleep_duration_hours: 8.0,
    time_zone: 'UTC',
    difficulty: 'Easy',
    productivity_goals: '',
    habit_preferences: 'Math,Memory,Logic'
  });

  const [alarms, setAlarms] = useState([]);
  const [newAlarmTime, setNewAlarmTime] = useState('07:00');
  const [newAlarmLabel, setNewAlarmLabel] = useState('Morning Alarm');
  const [newAlarmType, setNewAlarmType] = useState('Weekday');
  const [newAlarmSmart, setNewAlarmSmart] = useState(false);
  const [newAlarmDays, setNewAlarmDays] = useState('Monday,Tuesday,Wednesday,Thursday,Friday');

  // Analytics states
  const [stats, setStats] = useState({
    habit_score: 87.5,
    consistency_rate: 94.0,
    average_solve_time: 14.5,
    snooze_frequency: 0.8,
    score_history: [
      { id: 1, date: '2026-07-10', total_habit_score: 75.0, consistency_score: 80, completion_score: 90, snooze_score: 60, sleep_adherence_score: 70 },
      { id: 2, date: '2026-07-11', total_habit_score: 78.0, consistency_score: 82, completion_score: 92, snooze_score: 70, sleep_adherence_score: 72 },
      { id: 3, date: '2026-07-12', total_habit_score: 82.0, consistency_score: 85, completion_score: 88, snooze_score: 75, sleep_adherence_score: 80 },
      { id: 4, date: '2026-07-13', total_habit_score: 88.0, consistency_score: 90, completion_score: 92, snooze_score: 80, sleep_adherence_score: 90 },
      { id: 5, date: '2026-07-14', total_habit_score: 85.0, consistency_score: 82, completion_score: 95, snooze_score: 75, sleep_adherence_score: 90 },
      { id: 6, date: '2026-07-15', total_habit_score: 91.0, consistency_score: 95, completion_score: 94, snooze_score: 85, sleep_adherence_score: 90 },
      { id: 7, date: '2026-07-16', total_habit_score: 89.0, consistency_score: 90, completion_score: 90, snooze_score: 80, sleep_adherence_score: 95 },
      { id: 8, date: '2026-07-17', total_habit_score: 93.5, consistency_score: 96, completion_score: 98, snooze_score: 90, sleep_adherence_score: 90 }
    ],
    recent_challenges: [
      { id: 1, challenge_type: 'Math', difficulty: 'Easy', is_success: true, time_taken: 12.0 },
      { id: 2, challenge_type: 'Memory', difficulty: 'Medium', is_success: true, time_taken: 22.4 },
      { id: 3, challenge_type: 'Logic', difficulty: 'Hard', is_success: false, time_taken: 45.0 }
    ]
  });
  const [insights, setInsights] = useState({ insights: [], recommendations: [] });

  // Coach and Admin states
  const [coachData, setCoachData] = useState({ clients: [] });
  const [adminUsers, setAdminUsers] = useState([]);

  // Week 3 New States
  const [difficultyHistory, setDifficultyHistory] = useState([
    { id: 1, timestamp: '2026-07-15T07:05:00Z', previous_difficulty: 'Beginner', current_difficulty: 'Easy', reason: '5 consecutive correct solves' },
    { id: 2, timestamp: '2026-07-16T07:08:00Z', previous_difficulty: 'Easy', current_difficulty: 'Medium', reason: 'High speed alarm solving' }
  ]);
  const [currentAiDifficulty, setCurrentAiDifficulty] = useState('Medium');

  const [analyticsOverall, setAnalyticsOverall] = useState({
    average_wake_up_delay_minutes: 4.2,
    average_snooze_count: 0.8,
    average_sleep_duration_hours: 7.8,
    consistency_rate: 94.0,
    average_solve_time_seconds: 14.5,
    challenge_success_rate: 96.0,
    daily_productivity_score: 87.5
  });
  const [analyticsSleep, setAnalyticsSleep] = useState({
    average_sleep_duration: 7.8,
    sleep_adherence: 92.5,
    duration_trend_weekly: [7.2, 8.0, 7.5, 7.8, 8.2, 7.6, 7.8],
    duration_trend_monthly: [7.0, 7.2, 7.5, 8.0, 7.8, 8.2, 7.6, 7.8, 8.0, 7.5, 7.8, 8.2, 7.6, 7.8, 7.2, 8.0, 7.5, 7.8, 8.2, 7.6, 7.8, 8.0, 7.5, 7.8, 8.2, 7.6, 7.8, 7.2, 8.0, 7.8]
  });
  const [analyticsSnooze, setAnalyticsSnooze] = useState({
    average_snoozes: 0.8,
    snooze_counts: [1, 0, 2, 0, 1, 0, 1],
    total_alarms_dismissed: 14
  });
  const [analyticsProductivity, setAnalyticsProductivity] = useState({
    challenge_success_rate: 96.0,
    average_solve_time: 14.5,
    weekly_productivity_trend: [80, 82, 85, 88, 85, 91, 89, 93.5],
    monthly_productivity_trend: [72, 75, 70, 78, 80, 82, 85, 88, 85, 91, 89, 93.5, 72, 75, 70, 78, 80, 82, 85, 88, 85, 91, 89, 93.5, 80, 82, 85, 88, 85, 93.5]
  });

  const [recommendationsList, setRecommendationsList] = useState([
    { id: 1, category: 'Sleep', priority: 'High', title: 'Maintain Consistent Sleep Windows', description: 'Sleeping at the same hours each night regularizes your circadian rhythm, lowering morning wake-up delay.', reason: 'Your wake-up delays show higher fluctuations on weekends.', confidence: 92, is_saved: true, is_dismissed: false },
    { id: 2, category: 'Habit', priority: 'Medium', title: 'Limit Morning Alarm Snoozes', description: 'Snoozing fragments sleep, causing sleep inertia. Put your device further from your bed.', reason: 'You snoozed twice yesterday morning.', confidence: 85, is_saved: false, is_dismissed: false },
    { id: 3, category: 'Cognitive', priority: 'Low', title: 'Switch to Logic Challenge Puzzles', description: 'Logic puzzles activate the prefrontal cortex quickly, helping dismiss mental fog faster than math queries.', reason: 'Solve speed has stabilized on math levels.', confidence: 78, is_saved: false, is_dismissed: false }
  ]);
  const [activeDifficultyTab, setActiveDifficultyTab] = useState('current');
  const [analyticsTimeRange, setAnalyticsTimeRange] = useState('week');

  // Alarm Lockscreen Simulation states
  const [isAlarmActive, setIsAlarmActive] = useState(false);
  const [activeAlarm, setActiveAlarm] = useState(null);
  const [currentChallenge, setCurrentChallenge] = useState(null);
  const [userChallengeAnswer, setUserChallengeAnswer] = useState('');
  const [snoozeCount, setSnoozeCount] = useState(0);
  const [challengeStartTime, setChallengeStartTime] = useState(null);
  const [challengeMessage, setChallengeMessage] = useState('');
  const [challengeError, setChallengeError] = useState(false);

  // Audio Synthesizer ref (Web Audio API)
  const audioCtxRef = useRef(null);
  const audioIntervalRef = useRef(null);

  // Time ticking for simulation
  const [systemTime, setSystemTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      setSystemTime(now);

      // Auto-trigger alarm logic:
      // Loop over active alarms, match current HH:MM (when seconds are 0)
      if (token && !isAlarmActive && alarms.length > 0) {
        const currentHHMM = now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' });
        const dayName = now.toLocaleDateString('en-US', { weekday: 'long' });

        const matchingAlarm = alarms.find(alarm => {
          if (!alarm.is_active) return false;
          if (alarm.time !== currentHHMM) return false;

          // Days matching check
          const activeDays = alarm.days_of_week.split(',');
          return activeDays.includes(dayName);
        });

        if (matchingAlarm) {
          triggerAlarm(matchingAlarm);
        }
      }
    }, 1000);
    return () => clearInterval(timer);
  }, [token, alarms, isAlarmActive]);

  // Fetch data on login/tab change
  useEffect(() => {
    if (token) {
      fetchProfile();
      fetchAlarms();
      fetchDashboardStats();
      fetchInsights();
      fetchDifficulty();
      fetchRecommendations();
      fetchAnalyticsData();
      if (role === 'coach' || role === 'admin') fetchCoachClients();
      if (role === 'admin') fetchAdminUsers();
    }
  }, [token, activeTab]);

  // API Call Helpers
  const getHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  });

  const fetchProfile = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/profile`, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
      }
    } catch (e) { console.error("Error fetching profile", e); }
  };

  const fetchAlarms = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/alarms`, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setAlarms(data);
      }
    } catch (e) { console.error("Error fetching alarms", e); }
  };

  const fetchDashboardStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/dashboard/stats`, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setStats(data);
      }
    } catch (e) { console.error("Error fetching dashboard stats", e); }
  };

  const fetchInsights = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/dashboard/insights`, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setInsights(data);
      }
    } catch (e) { console.error("Error fetching insights", e); }
  };

  const fetchDifficulty = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/difficulty`, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setCurrentAiDifficulty(data.current_difficulty);
        setDifficultyHistory(data.history);
      }
    } catch (e) { console.error("Error fetching difficulty", e); }
  };

  const fetchRecommendations = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/recommendations`, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setRecommendationsList(data);
      }
    } catch (e) { console.error("Error fetching recommendations", e); }
  };

  const generateRecommendations = async () => {
    try {
      await fetch(`${API_BASE}/api/recommendations/generate`, { method: 'POST', headers: getHeaders() });
      fetchRecommendations();
    } catch (e) { console.error("Error generating recommendations", e); }
  };

  const saveRecommendation = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/api/recommendations/${id}/save`, { method: 'PUT', headers: getHeaders() });
      if (res.ok) fetchRecommendations();
    } catch (e) { console.error("Error saving recommendation", e); }
  };

  const dismissRecommendation = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/api/recommendations/${id}/dismiss`, { method: 'PUT', headers: getHeaders() });
      if (res.ok) fetchRecommendations();
    } catch (e) { console.error("Error dismissing recommendation", e); }
  };

  const fetchAnalyticsData = async () => {
    try {
      const [overallRes, sleepRes, snoozeRes, productivityRes] = await Promise.all([
        fetch(`${API_BASE}/api/analytics`, { headers: getHeaders() }),
        fetch(`${API_BASE}/api/analytics/sleep`, { headers: getHeaders() }),
        fetch(`${API_BASE}/api/analytics/snooze`, { headers: getHeaders() }),
        fetch(`${API_BASE}/api/analytics/productivity`, { headers: getHeaders() })
      ]);

      if (overallRes.ok) setAnalyticsOverall(await overallRes.json());
      if (sleepRes.ok) setAnalyticsSleep(await sleepRes.json());
      if (snoozeRes.ok) setAnalyticsSnooze(await snoozeRes.json());
      if (productivityRes.ok) setAnalyticsProductivity(await productivityRes.json());
    } catch (e) { console.error("Error fetching analytics data", e); }
  };

  const updateDifficultyManual = async (level) => {
    try {
      const res = await fetch(`${API_BASE}/api/difficulty?difficulty_level=${level}`, { method: 'PUT', headers: getHeaders() });
      if (res.ok) {
        fetchDifficulty();
        fetchProfile(); // reload profile in case diff changes
      }
    } catch (e) { console.error("Error manually updating difficulty", e); }
  };

  const fetchCoachClients = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/coach/clients`, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setCoachData(data);
      }
    } catch (e) { console.error("Error fetching coach clients", e); }
  };

  const fetchAdminUsers = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/admin/users`, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setAdminUsers(data);
      }
    } catch (e) { console.error("Error fetching admin users", e); }
  };


  // Auth Handlers
  const handleLogin = async (e) => {
    e.preventDefault();
    setAuthError('');
    try {
      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('role', data.role);
        localStorage.setItem('email', email);
        setToken(data.access_token);
        setRole(data.role);
        setPassword('');
      } else {
        const err = await res.json();
        setAuthError(err.detail || 'Login failed.');
      }
    } catch (e) {
      setAuthError('Connection error to FastAPI backend.');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setAuthError('');
    try {
      const res = await fetch(`${API_BASE}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, role })
      });
      if (res.ok) {
        setIsRegistering(false);
        alert('Registration successful! Please login.');
      } else {
        const err = await res.json();
        setAuthError(err.detail || 'Registration failed.');
      }
    } catch (e) {
      setAuthError('Connection error to FastAPI backend.');
    }
  };

  const handleGuestLogin = async () => {
    setAuthError('');
    const guestEmail = 'guest@alarm.com';
    const guestPassword = 'GuestPassword123!';
    const guestRole = 'user';

    try {
      let res = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: guestEmail, password: guestPassword })
      });

      if (!res.ok) {
        const regRes = await fetch(`${API_BASE}/api/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: guestEmail, password: guestPassword, role: guestRole })
        });

        if (regRes.ok) {
          res = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: guestEmail, password: guestPassword })
          });
        }
      }

      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('role', data.role);
        localStorage.setItem('email', guestEmail);
        setToken(data.access_token);
        setRole(data.role);
        setEmail(guestEmail);
        setPassword('');
      } else {
        setAuthError('Failed to sign in as guest.');
      }
    } catch (e) {
      setAuthError('Connection error to FastAPI backend.');
    }
  };


  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('email');
    setToken('');
    setRole('user');
    setEmail('');
    stopAlarmSound();
  };

  // Profile Save
  const handleSaveProfile = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE}/api/profile`, {
        method: 'PUT',
        headers: getHeaders(),
        body: JSON.stringify(profile)
      });
      if (res.ok) {
        alert('Profile saved successfully.');
        fetchProfile();
      }
    } catch (e) { console.error(e); }
  };

  // Alarm Operations
  const handleCreateAlarm = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE}/api/alarms`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({
          time: newAlarmTime,
          label: newAlarmLabel,
          is_active: true,
          is_smart_adaptive: newAlarmSmart,
          days_of_week: newAlarmDays,
          alarm_type: newAlarmType
        })
      });
      if (res.ok) {
        fetchAlarms();
        setNewAlarmLabel('Morning Alarm');
      }
    } catch (e) { console.error(e); }
  };

  const toggleAlarmStatus = async (alarm) => {
    try {
      await fetch(`${API_BASE}/api/alarms/${alarm.id}`, {
        method: 'PUT',
        headers: getHeaders(),
        body: JSON.stringify({ is_active: !alarm.is_active })
      });
      fetchAlarms();
    } catch (e) { console.error(e); }
  };

  const deleteAlarm = async (id) => {
    try {
      await fetch(`${API_BASE}/api/alarms/${id}`, {
        method: 'DELETE',
        headers: getHeaders()
      });
      fetchAlarms();
    } catch (e) { console.error(e); }
  };

  // Web Audio Synth for alarm ringtone
  const playAlarmSound = () => {
    try {
      if (!audioCtxRef.current) {
        audioCtxRef.current = new (window.AudioContext || window.webkitAudioContext)();
      }

      const playBeep = () => {
        if (!audioCtxRef.current) return;
        const osc = audioCtxRef.current.createOscillator();
        const gain = audioCtxRef.current.createGain();
        osc.connect(gain);
        gain.connect(audioCtxRef.current.destination);

        osc.frequency.value = 880; // High tone beep
        gain.gain.setValueAtTime(0.5, audioCtxRef.current.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtxRef.current.currentTime + 0.4);

        osc.start();
        osc.stop(audioCtxRef.current.currentTime + 0.5);
      };

      playBeep();
      audioIntervalRef.current = setInterval(playBeep, 1200);
    } catch (e) {
      console.warn("Audio Context blocked or failed", e);
    }
  };

  const stopAlarmSound = () => {
    if (audioIntervalRef.current) {
      clearInterval(audioIntervalRef.current);
      audioIntervalRef.current = null;
    }
    if (audioCtxRef.current) {
      audioCtxRef.current.close().catch(() => { });
      audioCtxRef.current = null;
    }
  };

  // Alarm simulated triggering
  const triggerAlarm = async (alarm) => {
    setActiveAlarm(alarm);
    setIsAlarmActive(true);
    setSnoozeCount(0);
    playAlarmSound();

    // Generate first chal
    generateChallengeForAlarm();
  };

  const generateChallengeForAlarm = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/challenges/generate`, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setCurrentChallenge(data);
        setChallengeStartTime(Date.now());
        setUserChallengeAnswer('');
        setChallengeMessage('');
        setChallengeError(false);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleSnooze = () => {
    setSnoozeCount(prev => prev + 1);

    // Alert / Toast effect
    setChallengeMessage(`Snoozed! Challenge difficulty adapted upwards. Avoid oversleeping!`);
    setChallengeError(true);

    // Refresh challenge immediately with a harder variant
    generateChallengeForAlarm();
  };

  const submitChallengeSolve = async () => {
    if (!currentChallenge) return;

    const timeTaken = (Date.now() - challengeStartTime) / 1000;

    try {
      const res = await fetch(
        `${API_BASE}/api/challenges/${currentChallenge.log_id}/solve?answer=${encodeURIComponent(userChallengeAnswer)}`,
        {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify({
            time_taken_seconds: timeTaken,
            snooze_count: snoozeCount,
            is_success: true // simulation success validation
          })
        }
      );

      if (res.ok) {
        const data = await res.json();
        setChallengeMessage(data.message);
        setChallengeError(false);

        // Turn off alarm and unlock
        setTimeout(() => {
          stopAlarmSound();
          setIsAlarmActive(false);
          setActiveAlarm(null);
          setCurrentChallenge(null);
          fetchDashboardStats();
          fetchProfile(); // reload profile in case difficulty shifted
        }, 1500);

      } else {
        setChallengeMessage("Incorrect answer. Please solve carefully!");
        setChallengeError(true);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Coach override difficulty handler
  const overrideClientDifficulty = async (clientId, level) => {
    try {
      const res = await fetch(`${API_BASE}/api/coach/clients/${clientId}/set-difficulty?difficulty_level=${level}`, {
        method: 'POST',
        headers: getHeaders()
      });
      if (res.ok) {
        alert(`Success: Difficulty adjusted to ${level}`);
        fetchCoachClients();
      }
    } catch (e) { console.error(e); }
  };

  // Export report
  const triggerExcelExport = () => {
    window.open(`${API_BASE}/api/reports/export?token=${token}`, '_blank');
  };

  // Authentication UI Render
  if (!token) {
    return (
      <div style={authStyles.wrapper}>
        <div className="glow-card" style={authStyles.container}>
          <div style={{ textAlign: 'center', marginBottom: 25 }}>
            <h1 style={{ fontSize: 28, color: '#818cf8', fontWeight: 700 }}>Cognitive Alarm</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14, marginTop: 4 }}>Wake up with cognitive intelligence</p>
          </div>

          {authError && <div style={authStyles.errorBadge}>{authError}</div>}

          <form onSubmit={isRegistering ? handleRegister : handleLogin}>
            <div style={{ marginBottom: 15 }}>
              <label style={authStyles.label}>Email Address</label>
              <input
                type="email"
                className="input-field"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
              />
            </div>

            <div style={{ marginBottom: 20 }}>
              <label style={authStyles.label}>Password</label>
              <input
                type="password"
                className="input-field"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
              />
            </div>

            {isRegistering && (
              <div style={{ marginBottom: 20 }}>
                <label style={authStyles.label}>Select Role</label>
                <select
                  className="input-field"
                  value={role}
                  onChange={e => setRole(e.target.value)}
                  style={{ background: '#1c1d28' }}
                >
                  <option value="user">User</option>
                  <option value="coach">Wellness Coach</option>
                  <option value="admin">Administrator</option>
                </select>
              </div>
            )}

            <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center' }}>
              {isRegistering ? 'Register Account' : 'Sign In'}
            </button>

            {!isRegistering && (
              <button
                type="button"
                onClick={handleGuestLogin}
                className="btn-secondary"
                style={{ width: '100%', justifyContent: 'center', marginTop: 10, borderColor: 'var(--color-secondary)', color: 'var(--color-secondary)' }}
              >
                Continue as Guest
              </button>
            )}
          </form>

          <div style={{ marginTop: 20, textAlign: 'center' }}>
            <span style={{ color: 'var(--text-dim)', fontSize: 14 }}>
              {isRegistering ? 'Already have an account? ' : "Don't have an account? "}
            </span>
            <button
              onClick={() => setIsRegistering(!isRegistering)}
              style={{ background: 'none', border: 'none', color: '#2dd4bf', cursor: 'pointer', fontWeight: 500 }}
            >
              {isRegistering ? 'Sign In' : 'Create Free Account'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={layoutStyles.wrapper}>
      {/* Sidebar Navigation */}
      <aside style={layoutStyles.sidebar}>
        <div style={layoutStyles.brandSection}>
          <h2 style={{ fontSize: 20, color: 'var(--color-primary)', fontWeight: 700 }}>Cognitive Alarm</h2>
          <span style={{ fontSize: 11, background: 'rgba(45, 212, 191, 0.1)', color: 'var(--color-secondary)', padding: '2px 8px', borderRadius: 10, marginTop: 4, display: 'inline-block' }}>
            {role.toUpperCase()}
          </span>
        </div>

        <nav style={layoutStyles.nav}>
          <button
            style={activeTab === 'dashboard' ? layoutStyles.activeNavItem : layoutStyles.navItem}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>

          <button
            style={activeTab === 'alarms' ? layoutStyles.activeNavItem : layoutStyles.navItem}
            onClick={() => setActiveTab('alarms')}
          >
            Smart Alarms ({alarms.length})
          </button>

          <button
            style={activeTab === 'difficulty' ? layoutStyles.activeNavItem : layoutStyles.navItem}
            onClick={() => setActiveTab('difficulty')}
          >
            Difficulty Settings
          </button>

          <button
            style={activeTab === 'recommendations' ? layoutStyles.activeNavItem : layoutStyles.navItem}
            onClick={() => setActiveTab('recommendations')}
          >
            Recommendations ({recommendationsList.filter(r => !r.is_dismissed).length})
          </button>

          <button
            style={activeTab === 'analytics' ? layoutStyles.activeNavItem : layoutStyles.navItem}
            onClick={() => setActiveTab('analytics')}
          >
            Behavioral Analytics
          </button>

          {(role === 'coach' || role === 'admin') && (
            <button
              style={activeTab === 'coach' ? layoutStyles.activeNavItem : layoutStyles.navItem}
              onClick={() => setActiveTab('coach')}
            >
              Wellness Portal
            </button>
          )}

          {role === 'admin' && (
            <button
              style={activeTab === 'admin' ? layoutStyles.activeNavItem : layoutStyles.navItem}
              onClick={() => setActiveTab('admin')}
            >
              Admin Dashboard
            </button>
          )}
        </nav>

        <div style={layoutStyles.sidebarFooter}>
          <span style={{ color: 'var(--text-dim)', fontSize: 13, display: 'block', marginBottom: 8 }}>{email}</span>
          <button onClick={handleLogout} className="btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main style={layoutStyles.mainContent}>
        {/* Dynamic header with clock */}
        <header style={layoutStyles.header}>
          <div>
            <h1 style={{ fontSize: 26, fontWeight: 600 }}>Welcome back, Wake-up Specialist</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Track consistency, elevate morning performance.</p>
          </div>
          <div style={layoutStyles.clockWidget}>
            <span style={{ fontSize: 24, fontWeight: 700, color: 'var(--color-secondary)' }}>
              {systemTime.toLocaleTimeString('en-US', { hour12: false })}
            </span>
            <span style={{ fontSize: 12, color: 'var(--text-dim)', marginLeft: 8 }}>
              {systemTime.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}
            </span>
          </div>
        </header>

        {/* Dynamic Content Views */}
        <div style={{ marginTop: 24 }}>
          {/* TAB 1: DASHBOARD */}
          {activeTab === 'dashboard' && (
            <div>
              {/* Stat grid */}
              <div style={dashboardStyles.grid3}>
                <div className="glow-card" style={dashboardStyles.statCard}>
                  <h3>Overall Habit Score</h3>
                  <div style={dashboardStyles.statNum}>{stats.habit_score}/100</div>
                  <p style={{ color: 'var(--text-muted)' }}>Target: 85+ consistency metric</p>
                </div>

                <div className="glow-card" style={dashboardStyles.statCard}>
                  <h3>Wake-up Consistency</h3>
                  <div style={dashboardStyles.statNum} className="color-teal">{stats.consistency_rate}%</div>
                  <p style={{ color: 'var(--text-muted)' }}>Average deviation to alarm</p>
                </div>

                <div className="glow-card" style={dashboardStyles.statCard}>
                  <h3>Average Solve Time</h3>
                  <div style={dashboardStyles.statNum} className="color-purple">{stats.average_solve_time}s</div>
                  <p style={{ color: 'var(--text-muted)' }}>Challenge validation speed</p>
                </div>
              </div>

              {/* Recommendation insight box */}
              <div className="glow-card" style={{ marginTop: 24, padding: 24 }}>
                <h2 style={{ color: 'var(--color-secondary)', fontSize: 18, marginBottom: 15 }}>AI Wake Up Insights</h2>
                {insights.insights.length === 0 ? (
                  <p style={{ color: 'var(--text-muted)' }}>No behavioral logs loaded yet. Perform challenge solves to populate reports.</p>
                ) : (
                  <div>
                    <ul style={{ paddingLeft: 18, color: 'var(--text-main)', marginBottom: 20 }}>
                      {insights.insights.map((ins, i) => <li key={i} style={{ marginBottom: 6 }}>{ins}</li>)}
                    </ul>
                    <h3 style={{ color: 'var(--color-primary)', fontSize: 15, marginBottom: 8 }}>Recommendations to improve routine:</h3>
                    <ul style={{ paddingLeft: 18, color: 'var(--text-muted)' }}>
                      {insights.recommendations.map((rec, i) => <li key={i} style={{ marginBottom: 6 }}>{rec}</li>)}
                    </ul>
                  </div>
                )}
              </div>

              {/* Quick Profile config */}
              <div style={dashboardStyles.grid2}>
                <div className="glow-card" style={{ padding: 24 }}>
                  <h2 style={{ fontSize: 18, marginBottom: 15 }}>Goal and Schedule Profile</h2>
                  <form onSubmit={handleSaveProfile}>
                    <div style={{ marginBottom: 12 }}>
                      <label style={authStyles.label}>Target Wake-up Time</label>
                      <input
                        type="text"
                        placeholder="HH:MM"
                        value={profile.preferred_wake_up_time}
                        onChange={e => setProfile({ ...profile, preferred_wake_up_time: e.target.value })}
                        className="input-field"
                      />
                    </div>
                    <div style={{ marginBottom: 12 }}>
                      <label style={authStyles.label}>Expected Sleep (Hours)</label>
                      <input
                        type="number"
                        step="0.5"
                        value={profile.sleep_duration_hours}
                        onChange={e => setProfile({ ...profile, sleep_duration_hours: parseFloat(e.target.value) })}
                        className="input-field"
                      />
                    </div>
                    <div style={{ marginBottom: 12 }}>
                      <label style={authStyles.label}>Current Difficulty</label>
                      <select
                        value={profile.difficulty}
                        onChange={e => setProfile({ ...profile, difficulty: e.target.value })}
                        className="input-field"
                        style={{ background: '#12131a' }}
                      >
                        <option value="Beginner">Beginner</option>
                        <option value="Easy">Easy</option>
                        <option value="Medium">Medium</option>
                        <option value="Hard">Hard</option>
                        <option value="Expert">Expert</option>
                      </select>
                    </div>
                    <div style={{ marginBottom: 12 }}>
                      <label style={authStyles.label}>Challenge Categories (comma split)</label>
                      <input
                        type="text"
                        value={profile.habit_preferences}
                        onChange={e => setProfile({ ...profile, habit_preferences: e.target.value })}
                        className="input-field"
                      />
                    </div>
                    <button type="submit" className="btn-primary">Update Profile Settings</button>
                  </form>
                </div>

                <div className="glow-card" style={{ padding: 24 }}>
                  <h2 style={{ fontSize: 18, marginBottom: 15 }}>Recent Challenge Logs</h2>
                  {stats.recent_challenges.length === 0 ? (
                    <p style={{ color: 'var(--text-muted)' }}>No completed challenge history.</p>
                  ) : (
                    <div style={{ overflowX: 'auto' }}>
                      <table style={tableStyles.table}>
                        <thead>
                          <tr>
                            <th>Type</th>
                            <th>Difficulty</th>
                            <th>Solve Time</th>
                            <th>Snoozes</th>
                            <th>Result</th>
                          </tr>
                        </thead>
                        <tbody>
                          {stats.recent_challenges.map(log => (
                            <tr key={log.id}>
                              <td>{log.challenge_type}</td>
                              <td>{log.difficulty}</td>
                              <td>{log.time_taken_seconds ? `${log.time_taken_seconds}s` : 'N/A'}</td>
                              <td>{log.snooze_count}</td>
                              <td>
                                <span style={{ color: log.is_success ? 'var(--color-success)' : 'var(--color-danger)' }}>
                                  {log.is_success ? 'Success' : 'Pending'}
                                </span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: SMART ALARMS */}
          {activeTab === 'alarms' && (
            <div style={dashboardStyles.grid2}>
              {/* Alarms Creater */}
              <div className="glow-card" style={{ padding: 24 }}>
                <h2 style={{ fontSize: 18, marginBottom: 15 }}>Schedule Multi-Alarm Plan</h2>
                <form onSubmit={handleCreateAlarm}>
                  <div style={{ marginBottom: 12 }}>
                    <label style={authStyles.label}>Trigger Time (HH:MM)</label>
                    <input
                      type="time"
                      value={newAlarmTime}
                      onChange={e => setNewAlarmTime(e.target.value)}
                      className="input-field"
                      required
                    />
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <label style={authStyles.label}>Alarm Label</label>
                    <input
                      type="text"
                      value={newAlarmLabel}
                      onChange={e => setNewAlarmLabel(e.target.value)}
                      className="input-field"
                    />
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <label style={authStyles.label}>Alarm Recurrence Pattern</label>
                    <select
                      value={newAlarmType}
                      onChange={e => setNewAlarmType(e.target.value)}
                      className="input-field"
                      style={{ background: '#12131a' }}
                    >
                      <option value="Weekday">Weekday Alarms</option>
                      <option value="Daily">Daily</option>
                      <option value="Weekend">Weekend</option>
                      <option value="One-Time">One-Time Only</option>
                      <option value="Smart Adaptive">Smart Adaptive</option>
                    </select>
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <label style={authStyles.label}>Active Days (comma separated check)</label>
                    <input
                      type="text"
                      value={newAlarmDays}
                      onChange={e => setNewAlarmDays(e.target.value)}
                      className="input-field"
                    />
                  </div>
                  <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 10 }}>
                    <input
                      type="checkbox"
                      checked={newAlarmSmart}
                      onChange={e => setNewAlarmSmart(e.target.checked)}
                    />
                    <label>Enable Smart Adaptive Difficulty override (scales difficulty with snooze counts)</label>
                  </div>
                  <button type="submit" className="btn-primary">Generate Alarm Segment</button>
                </form>
              </div>

              {/* Active Alarms list */}
              <div className="glow-card" style={{ padding: 24 }}>
                <h2 style={{ fontSize: 18, marginBottom: 15 }}>My Active Alarm Registry</h2>
                {alarms.length === 0 ? (
                  <p style={{ color: 'var(--text-muted)' }}>No alarms configured. Set up a regular wake up clock.</p>
                ) : (
                  <div style={{ display: 'grid', gap: 16 }}>
                    {alarms.map(alarm => (
                      <div key={alarm.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px', background: '#1c1d28', borderRadius: '8px', border: '1px solid var(--border-glass)' }}>
                        <div>
                          <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--color-primary)' }}>{alarm.time}</div>
                          <div style={{ fontWeight: 500, fontSize: 14 }}>{alarm.label} ({alarm.alarm_type})</div>
                          <div style={{ fontSize: 12, color: 'var(--text-dim)', marginTop: 4 }}>{alarm.days_of_week}</div>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                          <button
                            onClick={() => toggleAlarmStatus(alarm)}
                            className="btn-secondary"
                            style={{
                              padding: '6px 12px',
                              borderColor: alarm.is_active ? 'var(--color-success)' : 'var(--color-danger)',
                              color: alarm.is_active ? 'var(--color-success)' : 'var(--text-main)'
                            }}
                          >
                            {alarm.is_active ? 'Enabled' : 'Disabled'}
                          </button>

                          <button
                            onClick={() => triggerAlarm(alarm)}
                            className="btn-primary"
                            style={{ padding: '6px 12px', fontSize: 12 }}
                          >
                            Test Run
                          </button>

                          <button
                            onClick={() => deleteAlarm(alarm.id)}
                            style={{ border: 'none', background: 'none', color: '#f87171', cursor: 'pointer' }}
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* TAB 3: DIFFICULTY SETTINGS */}
          {activeTab === 'difficulty' && (
            <div className="glow-card" style={{ padding: 24 }}>
              <h2>AI Adaptive Difficulty Engine Settings</h2>
              <p style={{ color: 'var(--text-dim)', marginBottom: 20 }}>
                Our reinforcement learning loops scale difficulty upwards based on consistency triggers, and scale difficulty downwards on consecutive failures. Configure manually below.
              </p>

              <div style={{ display: 'flex', gap: 20, marginBottom: 30, flexWrap: 'wrap' }}>
                <div style={{ flex: 1, padding: 24, borderRadius: 12, border: '1px solid var(--border-glass)', background: 'rgba(0,0,0,0.15)', minWidth: 280 }}>
                  <h3 style={{ fontSize: 16, color: 'var(--text-muted)' }}>Current AI Calibrated Difficulty</h3>
                  <div style={{ fontSize: 48, fontWeight: 800, margin: '20px 0', color: 'var(--color-primary)' }}>{currentAiDifficulty}</div>

                  <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                    {['Beginner', 'Easy', 'Medium', 'Hard', 'Expert'].map(l => (
                      <button
                        key={l}
                        onClick={() => updateDifficultyManual(l)}
                        className={currentAiDifficulty === l ? 'btn-primary' : 'btn-secondary'}
                        style={{ padding: '8px 14px', fontSize: 13, textTransform: 'capitalize' }}
                      >
                        {l}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <h3>Difficulty Transition History</h3>
              {difficultyHistory.length === 0 ? (
                <p style={{ color: 'var(--text-muted)', marginTop: 15 }}>No difficulty updates logged. The AI engine automatically writes updates upon streaks.</p>
              ) : (
                <div style={{ overflowX: 'auto', marginTop: 15 }}>
                  <table style={tableStyles.table}>
                    <thead>
                      <tr>
                        <th>Timestamp</th>
                        <th>Previous Level</th>
                        <th>New Level</th>
                        <th>Reason / Trigger</th>
                      </tr>
                    </thead>
                    <tbody>
                      {difficultyHistory.map(h => (
                        <tr key={h.id}>
                          <td>{new Date(h.timestamp).toLocaleString()}</td>
                          <td style={{ color: 'var(--text-muted)' }}>{h.previous_difficulty}</td>
                          <td style={{ color: 'var(--color-secondary)', fontWeight: 650 }}>{h.current_difficulty}</td>
                          <td>{h.reason}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* TAB 3.5: BEHAVIORAL RECOMMENDATIONS */}
          {activeTab === 'recommendations' && (
            <div className="glow-card" style={{ padding: 24 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, flexWrap: 'wrap', gap: 10 }}>
                <div>
                  <h2>Personalized Routine Advice & Recommendations</h2>
                  <p style={{ color: 'var(--text-dim)' }}>AI-driven recommendations evaluated using pandas to enhance sleep hygiene.</p>
                </div>
                <button onClick={generateRecommendations} className="btn-primary">
                  Regenerate Insights
                </button>
              </div>

              {recommendationsList.length === 0 ? (
                <p style={{ color: 'var(--text-muted)' }}>No recommendation insights available. Generate recommendations to trigger rules.</p>
              ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 20 }}>
                  {recommendationsList.map(rec => {
                    const categoryColors = {
                      'Sleep': { bg: 'rgba(239, 68, 68, 0.1)', border: 'rgba(239, 68, 68, 0.3)', text: '#ef4444' },
                      'Routine': { bg: 'rgba(59, 130, 246, 0.1)', border: 'rgba(59, 130, 246, 0.3)', text: '#3b82f6' },
                      'Cognitive': { bg: 'rgba(139, 92, 246, 0.1)', border: 'rgba(139, 92, 246, 0.3)', text: '#8b5cf6' },
                      'Habit': { bg: 'rgba(16, 185, 129, 0.1)', border: 'rgba(16, 185, 129, 0.3)', text: '#10b981' }
                    };
                    const colors = categoryColors[rec.category] || { bg: 'rgba(255,255,255,0.05)', border: 'rgba(255,255,255,0.1)', text: '#fff' };
                    const priorityColor = rec.priority === 'High' ? '#f87171' : rec.priority === 'Medium' ? '#fbbf24' : '#2dd4bf';

                    return (
                      <div key={rec.id} className="glow-card" style={{ padding: 20, border: `1px solid ${colors.border}`, position: 'relative', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                        <div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                            <span style={{ fontSize: 11, background: colors.bg, color: colors.text, border: `1px solid ${colors.border}`, padding: '3px 8px', borderRadius: 12, fontWeight: 700 }}>
                              {rec.category}
                            </span>
                            <span style={{ fontSize: 11, color: priorityColor, fontWeight: 700 }}>
                              {rec.priority} Priority
                            </span>
                          </div>

                          <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 8, color: '#fff' }}>{rec.title}</h3>
                          <p style={{ color: 'var(--text-muted)', fontSize: 14, marginBottom: 15, lineHeight: 1.4 }}>{rec.description}</p>
                          <p style={{ fontSize: 12, color: 'var(--text-dim)', fontStyle: 'italic', marginBottom: 15 }}>Reason: {rec.reason}</p>
                        </div>

                        <div style={{ fontSize: 12, color: 'var(--text-dim)', borderTop: '1px solid var(--border-glass)', paddingTop: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <span>Confidence matches: {rec.confidence}%</span>
                          <div style={{ display: 'flex', gap: 8 }}>
                            <button
                              onClick={() => saveRecommendation(rec.id)}
                              className="btn-secondary"
                              style={{ padding: '6px 10px', fontSize: 11, borderColor: rec.is_saved ? 'var(--color-primary)' : 'var(--border-glass)', color: rec.is_saved ? 'var(--color-primary)' : '#fff' }}
                            >
                              {rec.is_saved ? '★ Saved' : '☆ Save'}
                            </button>
                            <button
                              onClick={() => dismissRecommendation(rec.id)}
                              className="btn-secondary"
                              style={{ padding: '6px 10px', fontSize: 11, color: '#f87171', border: '1px solid rgba(248,113,113,0.3)' }}
                            >
                              Dismiss
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {/* TAB 3.6: BEHAVIORAL ANALYTICS */}
          {activeTab === 'analytics' && (
            <div className="glow-card" style={{ padding: 24 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, flexWrap: 'wrap', gap: 10 }}>
                <div>
                  <h2>Behavioral Analytics Dashboard</h2>
                  <p style={{ color: 'var(--text-dim)' }}>Comprehensive reports on sleep trends, cognitive accuracy, and consistency patterns.</p>
                </div>
                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                  <button onClick={() => setAnalyticsTimeRange('week')} className={analyticsTimeRange === 'week' ? 'btn-primary' : 'btn-secondary'} style={{ padding: '8px 14px', fontSize: 12 }}>
                    Weekly
                  </button>
                  <button onClick={() => setAnalyticsTimeRange('month')} className={analyticsTimeRange === 'month' ? 'btn-primary' : 'btn-secondary'} style={{ padding: '8px 14px', fontSize: 12 }}>
                    Monthly
                  </button>
                  <button onClick={triggerExcelExport} className="btn-primary" style={{ padding: '8px 14px', fontSize: 12 }}>
                    Export Excel Reports
                  </button>
                </div>
              </div>

              {/* 4 Stats Cards */}
              <div style={{ ...dashboardStyles.grid3, marginBottom: 24 }}>
                <div className="glow-card" style={{ padding: 18, borderLeft: '4px solid #3b82f6', borderRadius: 8 }}>
                  <span style={{ fontSize: 12, color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: 1 }}>Avg Sleep Duration</span>
                  <h3 style={{ fontSize: 24, fontWeight: 700, margin: '8px 0', color: '#fff' }}>{analyticsSleep.average_sleep_duration} Hrs</h3>
                  <span style={{ fontSize: 11, color: '#10b981', fontWeight: 600 }}>{analyticsSleep.sleep_adherence}% Sleep Target Adherence</span>
                </div>

                <div className="glow-card" style={{ padding: 18, borderLeft: '4px solid #ef4444', borderRadius: 8 }}>
                  <span style={{ fontSize: 12, color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: 1 }}>Average Snooze Count</span>
                  <h3 style={{ fontSize: 24, fontWeight: 700, margin: '8px 0', color: '#fff' }}>{analyticsSnooze.average_snoozes} / Day</h3>
                  <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{analyticsSnooze.total_alarms_dismissed} Total Dismissed Alarms</span>
                </div>

                <div className="glow-card" style={{ padding: 18, borderLeft: '4px solid #8b5cf6', borderRadius: 8 }}>
                  <span style={{ fontSize: 12, color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: 1 }}>Cognitive Solve Speed</span>
                  <h3 style={{ fontSize: 24, fontWeight: 700, margin: '8px 0', color: '#fff' }}>{analyticsProductivity.average_solve_time}s</h3>
                  <span style={{ fontSize: 11, color: '#fbbf24', fontWeight: 600 }}>{analyticsProductivity.challenge_success_rate}% Puzzle Success Rate</span>
                </div>

                <div className="glow-card" style={{ padding: 18, borderLeft: '4px solid #10b981', borderRadius: 8 }}>
                  <span style={{ fontSize: 12, color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: 1 }}>Average Wake Delay</span>
                  <h3 style={{ fontSize: 24, fontWeight: 700, margin: '8px 0', color: '#fff' }}>{analyticsOverall.average_wake_up_delay_minutes} Min</h3>
                  <span style={{ fontSize: 11, color: '#10b981', fontWeight: 600 }}>Consistency baseline: {analyticsOverall.consistency_rate}%</span>
                </div>
              </div>

              {/* Custom SVG Charts */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: 24, marginBottom: 24 }}>
                <div className="glow-card" style={{ padding: 20 }}>
                  <h4 style={{ fontSize: 14, fontWeight: 650, color: 'var(--text-muted)', marginBottom: 12 }}>Routine Score Evolution (Daily Habit Scores)</h4>
                  <div style={{ height: 180, marginTop: 15, position: 'relative', borderLeft: '1px solid var(--border-glass)', borderBottom: '1px solid var(--border-glass)' }}>
                    {(() => {
                      const trend = analyticsTimeRange === 'week' ? analyticsProductivity.weekly_productivity_trend : analyticsProductivity.monthly_productivity_trend;
                      if (!trend || trend.length === 0) return null;
                      const width = 500;
                      const height = 180;
                      const points = trend.map((v, i) => {
                        const x = (i / (trend.length - 1)) * width;
                        const y = height - (v / 100) * height;
                        return `${x},${y}`;
                      });
                      const pathStr = `M ${points.join(' L ')}`;
                      const areaStr = `${pathStr} L ${width},${height} L 0,${height} Z`;
                      return (
                        <svg viewBox={`0 0 ${width} ${height}`} width="100%" height="100%" preserveAspectRatio="none">
                          <defs>
                            <linearGradient id="score-grad" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="0%" stopColor="var(--color-primary)" stopOpacity="0.3"></stop>
                              <stop offset="100%" stopColor="var(--color-primary)" stopOpacity="0.0"></stop>
                            </linearGradient>
                          </defs>
                          <path d={areaStr} fill="url(#score-grad)" />
                          <path d={pathStr} fill="none" stroke="var(--color-primary)" strokeWidth="3" linecap="round" />
                        </svg>
                      );
                    })()}
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: 11, color: 'var(--text-dim)' }}>
                    <span>{analyticsTimeRange === 'week' ? '7 days ago' : '30 days ago'}</span>
                    <span>Today</span>
                  </div>
                </div>

                <div className="glow-card" style={{ padding: 20 }}>
                  <h4 style={{ fontSize: 14, fontWeight: 650, color: 'var(--text-muted)', marginBottom: 12 }}>Circadian Sleep Duration Tracking (Hours)</h4>
                  <div style={{ height: 180, marginTop: 15, position: 'relative', borderLeft: '1px solid var(--border-glass)', borderBottom: '1px solid var(--border-glass)' }}>
                    {(() => {
                      const trend = analyticsTimeRange === 'week' ? analyticsSleep.duration_trend_weekly : analyticsSleep.duration_trend_monthly;
                      if (!trend || trend.length === 0) return null;
                      const width = 500;
                      const height = 180;
                      const points = trend.map((v, i) => {
                        const x = (i / (trend.length - 1)) * width;
                        const y = height - (v / 12) * height; // max 12 hours
                        return `${x},${y}`;
                      });
                      const pathStr = `M ${points.join(' L ')}`;
                      return (
                        <svg viewBox={`0 0 ${width} ${height}`} width="100%" height="100%" preserveAspectRatio="none">
                          <path d={pathStr} fill="none" stroke="var(--color-secondary)" strokeWidth="3" linecap="round" />
                        </svg>
                      );
                    })()}
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: 11, color: 'var(--text-dim)' }}>
                    <span>{analyticsTimeRange === 'week' ? '7 days ago' : '30 days ago'}</span>
                    <span>Today</span>
                  </div>
                </div>
              </div>

              {/* Heatmap Section */}
              <div style={{ marginTop: 20 }}>
                <h3 style={{ fontSize: 15, marginBottom: 10 }}>Circadian Calendar Heatmap</h3>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', padding: '16px', borderRadius: 8, background: '#13141f', border: '1px solid var(--border-glass)' }}>
                  {Array(30).fill(0).map((_, i) => {
                    const index = stats.score_history.length - 30 + i;
                    const hist = index >= 0 ? stats.score_history[index] : null;
                    const score = hist ? hist.total_habit_score : null;
                    let bgColor = '#1c1d28';
                    if (score !== null) {
                      if (score >= 90) bgColor = '#10b981';
                      else if (score >= 70) bgColor = '#3b82f6';
                      else if (score >= 50) bgColor = '#fbbf24';
                      else bgColor = '#ef4444';
                    }
                    return (
                      <div
                        key={i}
                        title={score !== null ? `Date: ${hist.date}\nScore: ${score}` : 'No Logged Score'}
                        style={{
                          width: 28,
                          height: 28,
                          borderRadius: 6,
                          backgroundColor: bgColor,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: 10,
                          fontWeight: 700,
                          cursor: 'pointer',
                          border: '1px solid rgba(255,255,255,0.05)',
                          color: score !== null ? '#000' : 'rgba(255,255,255,0.2)'
                        }}
                      >
                        {score !== null ? Math.round(score) : ''}
                      </div>
                    );
                  })}
                </div>
                <div style={{ display: 'flex', gap: 15, marginTop: 10, fontSize: 11, color: 'var(--text-muted)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}><div style={{ width: 12, height: 12, backgroundColor: '#10b981', borderRadius: 3 }} /> Excellent (90+)</div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}><div style={{ width: 12, height: 12, backgroundColor: '#3b82f6', borderRadius: 3 }} /> Good (70+)</div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}><div style={{ width: 12, height: 12, backgroundColor: '#fbbf24', borderRadius: 3 }} /> Caution (50+)</div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}><div style={{ width: 12, height: 12, backgroundColor: '#ef4444', borderRadius: 3 }} /> Critical (&lt;50)</div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: WELLNESS COACH PORTAL */}
          {activeTab === 'coach' && (
            <div className="glow-card" style={{ padding: 24 }}>
              <h2>Coached Client Overview</h2>
              <p style={{ color: 'var(--text-dim)', marginBottom: 20 }}>Inspect wake-up consistency patterns and adjust target puzzle difficulties.</p>

              {coachData.clients.length === 0 ? (
                <p style={{ color: 'var(--text-muted)' }}>No clients assigned. In production client tokens auto-register maps here.</p>
              ) : (
                <div style={{ overflowX: 'auto' }}>
                  <table style={tableStyles.table}>
                    <thead>
                      <tr>
                        <th>Client Email</th>
                        <th>Current Habit Score</th>
                        <th>Wake-up Consistency</th>
                        <th>Avg Solve Time</th>
                        <th>Avg Snoozes</th>
                        <th>Current Difficulty</th>
                        <th>Assign Difficulty Override</th>
                      </tr>
                    </thead>
                    <tbody>
                      {coachData.clients.map(client => (
                        <tr key={client.client_id}>
                          <td>{client.email}</td>
                          <td style={{ fontWeight: 600 }}>{client.current_habit_score}/100</td>
                          <td>{client.wake_up_consistency}%</td>
                          <td>{client.average_solve_time}s</td>
                          <td>{client.snooze_frequency}</td>
                          <td style={{ color: 'var(--color-secondary)' }}>{client.client_profile.difficulty}</td>
                          <td>
                            <select
                              onChange={(e) => overrideClientDifficulty(client.client_id, e.target.value)}
                              value={client.client_profile.difficulty}
                              style={{ padding: '4px 8px', border: '1px solid var(--border-glass)', background: '#1c1d28', color: '#fff', borderRadius: 4 }}
                            >
                              <option value="Beginner">Beginner</option>
                              <option value="Easy">Easy</option>
                              <option value="Medium">Medium</option>
                              <option value="Hard">Hard</option>
                              <option value="Expert">Expert</option>
                            </select>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* TAB 5: ADMIN DASHBOARD */}
          {activeTab === 'admin' && (
            <div className="glow-card" style={{ padding: 24 }}>
              <h2>Administrative Console</h2>
              <p style={{ color: 'var(--text-dim)', marginBottom: 20 }}>Modify user account settings, inspect logs, and toggle access configurations.</p>
              <div style={{ overflowX: 'auto' }}>
                <table style={tableStyles.table}>
                  <thead>
                    <tr>
                      <th>User ID</th>
                      <th>Email Address</th>
                      <th>Role Scope</th>
                      <th>Status Flag</th>
                      <th>Update Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {adminUsers.map(u => (
                      <tr key={u.id}>
                        <td>{u.id}</td>
                        <td>{u.email}</td>
                        <td>{u.role}</td>
                        <td style={{ color: u.is_active ? 'var(--color-success)' : 'var(--color-danger)' }}>
                          {u.is_active ? 'Active' : 'Suspended'}
                        </td>
                        <td>
                          <button
                            className="btn-secondary"
                            style={{ padding: '4px 8px', fontSize: 12 }}
                            onClick={async () => {
                              try {
                                await fetch(`${API_BASE}/api/admin/users/${u.id}`, {
                                  method: 'PUT',
                                  headers: getHeaders(),
                                  body: JSON.stringify({ is_active: !u.is_active })
                                });
                                fetchAdminUsers();
                              } catch (e) { console.error(e); }
                            }}
                          >
                            Toggle Status
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* FULLSCREEN CHALLENGE OVERLAY (ALARM TRIGGER LOCKSCREEN) */}
      {isAlarmActive && (
        <div style={alarmOverlayStyles.lockscreen}>
          <div className="glow-card" style={alarmOverlayStyles.challengeContainer}>
            <div style={{ textAlign: 'center', marginBottom: 24 }}>
              <div style={alarmOverlayStyles.alarmHeader}>🚨 ALARM RINDING 🚨</div>
              <h2 style={{ fontSize: 28, color: '#f87171', fontWeight: 700 }}>
                {activeAlarm ? activeAlarm.label : 'Wake Up!'} ({activeAlarm ? activeAlarm.time : ''})
              </h2>
              <p style={{ color: 'var(--text-muted)' }}>Dismiss by solving the puzzle below</p>
            </div>

            {challengeMessage && (
              <div style={{
                padding: '12px',
                borderRadius: '8px',
                backgroundColor: challengeError ? 'var(--color-danger-glow)' : 'rgba(52, 211, 153, 0.15)',
                color: challengeError ? 'var(--color-danger)' : 'var(--color-success)',
                border: `1px solid ${challengeError ? 'var(--color-danger)' : 'var(--color-success)'}`,
                marginBottom: 16,
                textAlign: 'center'
              }}>
                {challengeMessage}
              </div>
            )}

            {currentChallenge ? (
              <div style={alarmOverlayStyles.puzzleBox}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                  <span style={{ fontSize: 12, background: 'rgba(129, 140, 248, 0.2)', padding: '2px 8px', borderRadius: 4 }}>
                    Type: {currentChallenge.type}
                  </span>
                  <span style={{ fontSize: 12, background: 'rgba(251, 191, 36, 0.2)', padding: '2px 8px', borderRadius: 4 }}>
                    Difficulty: {currentChallenge.difficulty}
                  </span>
                </div>

                <h3 style={{ fontSize: 20, marginBottom: 20, lineHeight: 1.5, textAlign: 'center' }}>
                  {currentChallenge.question}
                </h3>

                {currentChallenge.options ? (
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 16 }}>
                    {currentChallenge.options.map((opt, i) => (
                      <button
                        key={i}
                        className="btn-secondary"
                        onClick={() => setUserChallengeAnswer(opt)}
                        style={{
                          padding: '12px',
                          textAlign: 'center',
                          background: userChallengeAnswer === opt ? 'rgba(45, 212, 191, 0.15)' : '',
                          borderColor: userChallengeAnswer === opt ? 'var(--color-secondary)' : ''
                        }}
                      >
                        {opt}
                      </button>
                    ))}
                  </div>
                ) : (
                  <input
                    type="text"
                    placeholder="Enter Solution..."
                    className="input-field"
                    value={userChallengeAnswer}
                    onChange={e => setUserChallengeAnswer(e.target.value)}
                    style={{ marginBottom: 16, fontSize: 18, textAlign: 'center' }}
                  />
                )}

                <div style={{ display: 'flex', gap: 16, marginTop: 20 }}>
                  <button
                    onClick={handleSnooze}
                    className="btn-secondary"
                    style={{ flex: 1, borderColor: '#f87171', color: '#f87171', justifyContent: 'center' }}
                  >
                    Snooze ({snoozeCount})
                  </button>

                  <button
                    onClick={submitChallengeSolve}
                    className="btn-primary"
                    style={{ flex: 1, justifyContent: 'center' }}
                  >
                    Submit Code
                  </button>
                </div>
              </div>
            ) : (
              <p style={{ textAlign: 'center', color: 'var(--text-muted)' }}>Querying dynamic challenge from cognitive backend engine...</p>
            )}

            <div style={{ textAlign: 'center', marginTop: 15, fontSize: 12, color: 'var(--text-dim)' }}>
              Note: Snoozing locks device and adapts next challenge difficulty upwards.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Inline Styles to guarantee layout styling behaves identical on all machines
const authStyles = {
  wrapper: {
    height: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'radial-gradient(circle at center, #11131c 0%, #090a0f 100%)',
    padding: 20,
  },
  container: {
    width: '100%',
    maxWidth: 420,
    padding: 35,
    borderRadius: 16,
    backgroundColor: '#12131a',
  },
  label: {
    display: 'block',
    fontSize: 13,
    fontWeight: 500,
    marginBottom: 6,
    color: 'var(--text-muted)'
  },
  errorBadge: {
    backgroundColor: 'var(--color-danger-glow)',
    border: '1px solid var(--color-danger)',
    color: 'var(--color-danger)',
    padding: '10px 14px',
    borderRadius: 8,
    marginBottom: 16,
    fontSize: 14,
    textAlign: 'center'
  }
};

const layoutStyles = {
  wrapper: {
    display: 'flex',
    minHeight: '100vh',
    background: 'var(--bg-primary)'
  },
  sidebar: {
    width: 250,
    maxHeight: '100vh',
    borderRight: '1px solid var(--border-glass)',
    display: 'flex',
    flexDirection: 'column',
    position: 'sticky',
    top: 0,
    backgroundColor: 'rgba(18, 19, 26, 0.5)',
    backdropFilter: 'blur(20px)',
    padding: '24px 16px'
  },
  brandSection: {
    padding: '12px 8px',
    borderBottom: '1px solid var(--border-glass)',
    marginBottom: 24
  },
  nav: {
    display: 'flex',
    flexDirection: 'column',
    gap: 8,
    flex: 1
  },
  navItem: {
    padding: '12px 14px',
    borderRadius: 8,
    border: 'none',
    background: 'none',
    color: 'var(--text-muted)',
    fontFamily: 'var(--font-sans)',
    fontSize: 15,
    fontWeight: 500,
    textAlign: 'left',
    cursor: 'pointer',
    transition: 'var(--transition-smooth)'
  },
  activeNavItem: {
    padding: '12px 14px',
    borderRadius: 8,
    border: 'none',
    background: 'rgba(129, 140, 248, 0.1)',
    color: 'var(--color-primary)',
    fontFamily: 'var(--font-sans)',
    fontSize: 15,
    fontWeight: 600,
    textAlign: 'left',
    cursor: 'pointer',
    borderLeft: '3px solid var(--color-primary)'
  },
  sidebarFooter: {
    padding: '12px 8px',
    borderTop: '1px solid var(--border-glass)'
  },
  mainContent: {
    flex: 1,
    padding: '40px',
    maxHeight: '100vh',
    overflowY: 'auto'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingBottom: 20,
    borderBottom: '1px solid var(--border-glass)'
  },
  clockWidget: {
    display: 'flex',
    alignItems: 'center',
    backgroundColor: '#12131a',
    padding: '12px 20px',
    borderRadius: 12,
    border: '1px solid var(--border-glass)'
  }
};

const dashboardStyles = {
  grid3: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: 20
  },
  grid2: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
    gap: 24,
    marginTop: 24
  },
  statCard: {
    padding: 24,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    minHeight: 140
  },
  statNum: {
    fontSize: 42,
    fontWeight: 700,
    color: 'var(--color-primary)',
    margin: '12px 0 4px 0'
  }
};

const tableStyles = {
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: 10,
    fontSize: 14,
    color: 'var(--text-main)'
  }
};

const alarmOverlayStyles = {
  lockscreen: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(9, 10, 15, 0.95)',
    backdropFilter: 'blur(30px)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 9999,
    padding: 20
  },
  challengeContainer: {
    width: '100%',
    maxWidth: 550,
    padding: 40,
    backgroundColor: '#12131a',
    border: '1px solid rgba(248, 113, 113, 0.25)', // slight red alarm border tint
  },
  alarmHeader: {
    fontSize: 16,
    color: '#f87171',
    fontWeight: 700,
    letterSpacing: 2,
    marginBottom: 8,
    animation: 'pulse 1s infinite'
  },
  puzzleBox: {
    backgroundColor: 'rgba(0,0,0,0.2)',
    border: '1px solid var(--border-glass)',
    borderRadius: 8,
    padding: 20
  }
};

export default App;
