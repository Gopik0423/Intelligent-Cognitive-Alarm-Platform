import { useEffect, useState } from "react";
import API from "../services/api";
import { Moon, AlarmClock, Zap, Heart } from "lucide-react";

function Section({ title, tips, color, Icon, iconColor }) {
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
      <h4 style={{ marginBottom: "10px", display: "flex", alignItems: "center", gap: "8px" }}>
        <Icon size={18} color={iconColor} />
        {title}
      </h4>
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
    return (
      <div className="spinner-wrap">
        <div className="spinner" />
      </div>
    );
  }

  return (
    <div style={{ width: "650px", margin: "40px auto" }}>
      <h2>Your Personalized Recommendations</h2>

      <Section title="Sleep" tips={data.sleep} color="var(--accent-blue)" Icon={Moon} iconColor="var(--icon-blue)" />
      <Section title="Wake-Up" tips={data.wake_up} color="var(--accent-orange)" Icon={AlarmClock} iconColor="var(--icon-orange)" />
      <Section title="Productivity" tips={data.productivity} color="var(--accent-green)" Icon={Zap} iconColor="var(--icon-green)" />
      <Section title="Habit" tips={data.habit} color="var(--accent-purple)" Icon={Heart} iconColor="var(--icon-purple)" />
    </div>
  );
}

export default Recommendation;
