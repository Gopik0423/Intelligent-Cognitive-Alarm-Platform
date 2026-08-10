import { useEffect, useState } from "react";
import API from "../services/api";
import { Feather, Zap, Flame, AlertTriangle } from "lucide-react";

const LEVEL_LABELS = { 1: "Easy", 2: "Easy", 3: "Medium", 4: "Hard" };
const SEGMENT_LABELS = ["Easy", "Easy", "Medium", "Hard"];

const TIER_ICON = {
  Easy: Feather,
  Medium: Zap,
  Hard: Flame,
};

function Difficulty() {
  const [difficulty, setDifficulty] = useState(null);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    init();
  }, []);

  const init = async () => {
    try {
      const userRes = await API.get("/user");
      setUserId(userRes.data.id);
      const res = await API.get(`/difficulty/get?user_id=${userRes.data.id}`);
      setDifficulty(res.data);
    } catch (err) {
      console.log(err.response?.data || err.message);
    }
  };

  if (!difficulty) {
    return (
      <div className="spinner-wrap">
        <div className="spinner" />
      </div>
    );
  }

  const tierLabel = LEVEL_LABELS[difficulty.difficulty_level];
  const TierIcon = TIER_ICON[tierLabel] || Feather;

  return (
    <div
      className="app-card"
      style={{
        width: "500px",
        margin: "40px auto",
        padding: "28px",
        textAlign: "center",
      }}
    >
      <h2>Difficulty Level</h2>

      <p style={{ fontSize: "14px", color: "var(--text-muted)" }}>
        Your difficulty adjusts automatically: 3 correct answers in a row
        raises it, 2 wrong answers in a row lowers it. This same level now
        applies to real alarms too, not just practice puzzles.
      </p>

      <TierIcon size={42} color="var(--primary)" style={{ marginTop: "12px" }} />

      <h1 style={{ fontSize: "48px", color: "var(--primary)", margin: "8px 0 4px" }}>
        {tierLabel}
      </h1>

      <div className="level-meter">
        {[1, 2, 3, 4].map((lvl) => (
          <div key={lvl} className="level-segment">
            <div className={`level-segment-bar ${lvl <= difficulty.difficulty_level ? "filled" : ""}`} />
            <div className="level-segment-label">{SEGMENT_LABELS[lvl - 1]}</div>
          </div>
        ))}
      </div>

      <p style={{ color: "var(--text-muted)", marginBottom: "8px", display: "flex", alignItems: "center", justifyContent: "center", gap: "8px" }}>
        <Flame size={16} color="var(--icon-orange)" />
        <b style={{ color: "var(--text)" }}>Correct streak:</b> {difficulty.correct_streak}
      </p>
      <p style={{ color: "var(--text-muted)", display: "flex", alignItems: "center", justifyContent: "center", gap: "8px" }}>
        <AlertTriangle size={16} color="var(--danger)" />
        <b style={{ color: "var(--text)" }}>Fail streak:</b> {difficulty.fail_streak}
      </p>
    </div>
  );
}

export default Difficulty;
