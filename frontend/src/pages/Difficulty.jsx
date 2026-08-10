import { useEffect, useState } from "react";
import API from "../services/api";

const LEVEL_LABELS = { 1: "Easy", 2: "Easy", 3: "Medium", 4: "Hard" };

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

  const setLevel = async (level) => {
    try {
      await API.post("/difficulty/update", {
        user_id: userId,
        action: "set",
        level: level,
      });
      const res = await API.get(`/difficulty/get?user_id=${userId}`);
      setDifficulty(res.data);
    } catch (err) {
      console.log(err.response?.data || err.message);
    }
  };

  if (!difficulty) {
    return <p style={{ textAlign: "center", marginTop: "40px", color: "var(--text-muted)" }}>Loading...</p>;
  }

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

      <h1 style={{ fontSize: "48px", color: "var(--primary)" }}>
        {LEVEL_LABELS[difficulty.difficulty_level]}
      </h1>

      <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}><b style={{ color: "var(--text)" }}>Level:</b> {difficulty.difficulty_level} / 4</p>
      <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}><b style={{ color: "var(--text)" }}>Correct streak:</b> {difficulty.correct_streak}</p>
      <p style={{ color: "var(--text-muted)" }}><b style={{ color: "var(--text)" }}>Fail streak:</b> {difficulty.fail_streak}</p>

      <hr style={{ border: "none", borderTop: "1px solid var(--border)", margin: "20px 0" }} />

      <p style={{ fontSize: "13px", color: "var(--text-muted)" }}>
        Manual override (for testing):
      </p>

      <div>
        {[1, 2, 3, 4].map((lvl) => (
          <button
            key={lvl}
            onClick={() => setLevel(lvl)}
            style={{
              margin: "5px",
              padding: "9px 16px",
              background: difficulty.difficulty_level === lvl ? "var(--primary)" : "var(--surface-alt)",
              color: difficulty.difficulty_level === lvl ? "var(--primary-contrast)" : "var(--text)",
              border: "1px solid var(--border)",
              borderRadius: "8px",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            {lvl} - {LEVEL_LABELS[lvl]}
          </button>
        ))}
      </div>
    </div>
  );
}

export default Difficulty;
