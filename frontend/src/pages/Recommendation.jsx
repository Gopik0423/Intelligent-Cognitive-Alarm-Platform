import { useEffect, useState } from "react";
import API from "../services/api";

function Section({ title, tips, color }) {
  return (
    <div
      style={{
        background: color,
        padding: "18px",
        borderRadius: "var(--radius)",
        border: "1px solid var(--border)",
        marginBottom: "16px",
      }}
    >
      <h4 style={{ marginBottom: "10px" }}>{title}</h4>
      <ul style={{ color: "var(--text-muted)", paddingLeft: "20px", margin: 0 }}>
        {tips.map((tip, i) => (
          <li key={i} style={{ marginBottom: "4px" }}>{tip}</li>
        ))}
      </ul>
    </div>
  );
}

function Recommendation() {
  const [data, setData] = useState(null);

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    try {
      const userRes = await API.get("/user");
      const res = await API.get(`/recommendation/${userRes.data.id}/full`);
      setData(res.data);
    } catch (err) {
      console.log(err.response?.data || err.message);
    }
  };

  if (!data) {
    return <p style={{ textAlign: "center", marginTop: "40px", color: "var(--text-muted)" }}>Loading...</p>;
  }

  return (
    <div style={{ width: "650px", margin: "40px auto" }}>
      <h2>Your Personalized Recommendations</h2>

      <Section title="Sleep" tips={data.sleep} color="var(--accent-blue)" />
      <Section title="Wake-Up" tips={data.wake_up} color="var(--accent-orange)" />
      <Section title="Productivity" tips={data.productivity} color="var(--accent-green)" />
      <Section title="Habit" tips={data.habit} color="var(--accent-purple)" />
    </div>
  );
}

export default Recommendation;
