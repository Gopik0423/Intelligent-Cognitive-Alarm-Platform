import { useEffect, useState } from "react";
import API from "../services/api";
import { Sun, Moon, User, Heart, Feather, Zap, Flame, Brain, TrendingDown, TrendingUp, Minus, ShieldCheck } from "lucide-react";

const TIER_ICON = {
  Easy: Feather,
  Medium: Zap,
  Hard: Flame,
};

function Dashboard() {

  const [user, setUser] = useState({});
  const [habitScore, setHabitScore] = useState(0);
  const [recommendation, setRecommendation] = useState("");
  const [analytics, setAnalytics] = useState({});
  const [difficulty, setDifficulty] = useState({});
  const [intelligence, setIntelligence] = useState(null);

  useEffect(() => {
    getDashboard();
  }, []);

  const getDashboard = async () => {
    try {
      const userRes = await API.get("/user");
      setUser(userRes.data);
      const userId = userRes.data.id;

      const habitRes = await API.get(`/habit-score?user_id=${userId}`);
      setHabitScore(habitRes.data.habit_score || 0);

      const difficultyRes = await API.get(`/difficulty/get?user_id=${userId}`);
      setDifficulty(difficultyRes.data);

      const recRes = await API.get(`/recommendation/${userId}`);
      setRecommendation(
        (recRes.data.recommendations && recRes.data.recommendations.join(" ")) ||
        recRes.data.message ||
        ""
      );

      const analyticsRes = await API.get(`/analytics/${userId}`);
      setAnalytics(analyticsRes.data);

      const intelligenceRes = await API.get(`/recommendation/${userId}/alarm-intelligence`);
      setIntelligence(intelligenceRes.data);
    } catch (err) {
      console.log("Dashboard Error:", err.response?.data || err.message);
    }
  };

  const difficultyLabel = (level) => {
    if (level >= 4) return "Hard";
    if (level === 3) return "Medium";
    return "Easy";
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return { text: "Good morning", Icon: Sun };
    if (hour < 18) return { text: "Good afternoon", Icon: Sun };
    return { text: "Good evening", Icon: Moon };
  };

  const { text: greetingText, Icon: GreetingIcon } = getGreeting();
  const tierLabel = difficultyLabel(difficulty.difficulty_level);
  const TierIcon = TIER_ICON[tierLabel] || Feather;
  const TrendIcon = intelligence?.behavior?.snooze_trend === "improving"
    ? TrendingUp
    : intelligence?.behavior?.snooze_trend === "declining" ? TrendingDown : Minus;

  const cardStyle = {
    flex: 1,
    padding: "22px",
    borderRadius: "var(--radius)",
    border: "1px solid var(--border)",
  };

  return (
    <div style={{ width: "80%", margin: "30px auto" }}>
      <h1 style={{ fontSize: "28px", display: "flex", alignItems: "center", gap: "10px" }}>
        <GreetingIcon size={26} color="var(--primary)" />
        {greetingText}{user.name ? `, ${user.name}` : ""}
      </h1>
      <hr style={{ border: "none", borderTop: "1px solid var(--border)" }} />

      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>

        <div className="app-card-hover" style={{ ...cardStyle, background: "var(--accent-blue)" }}>
          <h3 style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <User size={18} color="var(--icon-blue)" />
            User
          </h3>
          <p style={{ color: "var(--text-muted)", marginBottom: "6px" }}><b style={{ color: "var(--text)" }}>Name:</b> {user.name}</p>
          <p style={{ color: "var(--text-muted)", marginBottom: "6px" }}><b style={{ color: "var(--text)" }}>Role:</b> {user.role}</p>
          <p style={{ color: "var(--text-muted)" }}><b style={{ color: "var(--text)" }}>Email:</b> {user.email}</p>
        </div>

        <div className="app-card-hover" style={{ ...cardStyle, background: "var(--accent-orange)" }}>
          <h3 style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <Heart size={18} color="var(--icon-orange)" />
            Habit Score
          </h3>
          <h1 style={{ fontSize: "40px" }}>{habitScore}%</h1>
        </div>

        <div className="app-card-hover" style={{ ...cardStyle, background: "var(--accent-purple)" }}>
          <h3 style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <TierIcon size={18} color="var(--icon-purple)" />
            Difficulty Level
          </h3>
          <h1 style={{ fontSize: "40px" }}>{tierLabel}</h1>
          <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}><b style={{ color: "var(--text)" }}>Level:</b> {difficulty.difficulty_level ?? "-"} / 4</p>
          <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}><b style={{ color: "var(--text)" }}>Correct streak:</b> {difficulty.correct_streak ?? 0}</p>
          <p style={{ color: "var(--text-muted)" }}><b style={{ color: "var(--text)" }}>Fail streak:</b> {difficulty.fail_streak ?? 0}</p>
        </div>

      </div>

      <br />

      <div className="intelligence-panel">
        <div className="intelligence-heading">
          <div>
            <p className="intelligence-eyebrow"><Brain size={16} /> LIVE INTELLIGENCE</p>
            <h2>Alarm Intelligence</h2>
            <p>Your alarm adapts from every practice and wake-up verification attempt.</p>
          </div>
          <div className="validated-badge"><ShieldCheck size={16} /> {intelligence?.validated ? "Validated guidance" : "Loading guidance"}</div>
        </div>

        <div className="intelligence-grid">
          <div className="intelligence-stat">
            <span>Active challenge level</span>
            <strong>{intelligence?.current_difficulty || tierLabel}</strong>
            <small>Level {intelligence?.difficulty_level ?? difficulty.difficulty_level ?? 1} of 4</small>
          </div>
          <div className="intelligence-stat">
            <span>Behavior signal</span>
            <strong style={{ textTransform: "capitalize", display: "flex", alignItems: "center", gap: "6px" }}><TrendIcon size={20} /> {intelligence?.behavior?.snooze_trend || "Collecting data"}</strong>
            <small>Snooze trend</small>
          </div>
          <div className="intelligence-stat">
            <span>Attempts analyzed</span>
            <strong>{intelligence?.behavior?.records_analyzed ?? 0}</strong>
            <small>Need 4 for behavioral trends</small>
          </div>
        </div>

        <div className="intelligence-actions">
          <h3>Recommended next action</h3>
          {intelligence?.recommendations?.length ? intelligence.recommendations.map((item) => (
            <div className="intelligence-action" key={item.action}>
              <span className={`priority-dot ${item.priority}`} />
              <div><b>{item.action.replaceAll("_", " ")}</b><p>{item.reason}</p></div>
            </div>
          )) : <p>Complete a challenge to generate personalized alarm guidance.</p>}
        </div>
      </div>

      <br />

      <div style={{ ...cardStyle, background: "var(--accent-green)" }}>
        <h3>Today's Recommendation</h3>
        <p style={{ color: "var(--text-muted)" }}>{recommendation}</p>
      </div>

      <br />

      <div style={{ ...cardStyle, background: "var(--accent-pink)" }}>
        <h3>Analytics</h3>
        <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}><b style={{ color: "var(--text)" }}>Average Score :</b> {analytics.average_score ?? 0}</p>
        <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}><b style={{ color: "var(--text)" }}>Average Completion Time :</b> {analytics.average_completion_time ?? 0}s</p>
        <p style={{ color: "var(--text-muted)" }}><b style={{ color: "var(--text)" }}>Success Rate :</b> {analytics.success_rate ?? 0}%</p>
      </div>

    </div>
  );
}

export default Dashboard;
