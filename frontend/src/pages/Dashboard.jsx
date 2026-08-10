import { useEffect, useState } from "react";
import API from "../services/api";

function Dashboard() {

  const [user, setUser] = useState({});
  const [habitScore, setHabitScore] = useState(0);
  const [recommendation, setRecommendation] = useState("");
  const [analytics, setAnalytics] = useState({});
  const [difficulty, setDifficulty] = useState({});

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
    } catch (err) {
      console.log("Dashboard Error:", err.response?.data || err.message);
    }
  };

  const difficultyLabel = (level) => {
    if (level >= 4) return "Hard";
    if (level === 3) return "Medium";
    return "Easy";
  };

  const cardStyle = {
    flex: 1,
    padding: "22px",
    borderRadius: "var(--radius)",
    border: "1px solid var(--border)",
  };

  return (
    <div style={{ width: "80%", margin: "30px auto" }}>
      <h1 style={{ fontSize: "28px" }}>Cognitive Alarm Dashboard</h1>
      <hr style={{ border: "none", borderTop: "1px solid var(--border)" }} />

      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>

        <div style={{ ...cardStyle, background: "var(--accent-blue)" }}>
          <h3>User</h3>
          <p style={{ color: "var(--text-muted)", marginBottom: "6px" }}><b style={{ color: "var(--text)" }}>Name:</b> {user.name}</p>
          <p style={{ color: "var(--text-muted)", marginBottom: "6px" }}><b style={{ color: "var(--text)" }}>Role:</b> {user.role}</p>
          <p style={{ color: "var(--text-muted)" }}><b style={{ color: "var(--text)" }}>Email:</b> {user.email}</p>
        </div>

        <div style={{ ...cardStyle, background: "var(--accent-orange)" }}>
          <h3>Habit Score</h3>
          <h1 style={{ fontSize: "40px" }}>{habitScore}%</h1>
        </div>

        <div style={{ ...cardStyle, background: "var(--accent-purple)" }}>
          <h3>Difficulty Level</h3>
          <h1 style={{ fontSize: "40px" }}>{difficultyLabel(difficulty.difficulty_level)}</h1>
          <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}><b style={{ color: "var(--text)" }}>Level:</b> {difficulty.difficulty_level ?? "-"} / 4</p>
          <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}><b style={{ color: "var(--text)" }}>Correct streak:</b> {difficulty.correct_streak ?? 0}</p>
          <p style={{ color: "var(--text-muted)" }}><b style={{ color: "var(--text)" }}>Fail streak:</b> {difficulty.fail_streak ?? 0}</p>
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
