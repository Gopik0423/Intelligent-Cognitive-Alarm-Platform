import { useEffect, useState } from "react";
import API from "../services/api";

const TREND_COLOR = {
  improving: "var(--success)",
  declining: "var(--danger)",
  stable: "var(--text-muted)",
};

function TrendRow({ label, value }) {
  return (
    <p style={{ marginBottom: "6px" }}>
      <b style={{ color: "var(--text)" }}>{label}:</b>{" "}
      <span style={{ color: TREND_COLOR[value] || "var(--text)", fontWeight: 700 }}>
        {value}
      </span>
    </p>
  );
}

function BehaviorAnalytics() {
  const [data, setData] = useState(null);

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    try {
      const userRes = await API.get("/user");
      const res = await API.get(`/analytics/${userRes.data.id}/behavior`);
      setData(res.data);
    } catch (err) {
      console.log(err.response?.data || err.message);
    }
  };

  if (!data) {
    return <p style={{ textAlign: "center", marginTop: "40px", color: "var(--text-muted)" }}>Loading...</p>;
  }

  if (data.status === "not_enough_data") {
    return (
      <div className="app-card" style={{ width: "500px", margin: "40px auto", padding: "28px", textAlign: "center" }}>
        <h2>Behavioral Analytics</h2>
        <p style={{ color: "var(--text-muted)" }}>{data.message}</p>
      </div>
    );
  }

  return (
    <div
      className="app-card"
      style={{
        width: "500px",
        margin: "40px auto",
        padding: "28px",
      }}
    >
      <h2>Behavioral Analytics</h2>

      <p style={{ color: "var(--text-muted)" }}>Based on {data.records_analyzed} recent attempts</p>

      <div style={{ marginTop: "16px" }}>
        <TrendRow label="Snooze trend" value={data.snooze_trend} />
        <TrendRow label="Accuracy trend" value={data.accuracy_trend} />
        <TrendRow label="Wake-up consistency trend" value={data.wakeup_consistency_trend} />
      </div>

      <p style={{ marginTop: "12px" }}>
        <b style={{ color: "var(--text)" }}>Snooze / accuracy correlation:</b>{" "}
        <span style={{ color: "var(--text-muted)" }}>{data.snooze_accuracy_correlation ?? "not enough variation yet"}</span>
      </p>
      <p style={{ fontSize: "13px", color: "var(--text-muted)" }}>{data.correlation_note}</p>

      <p><b style={{ color: "var(--text)" }}>Most common challenge type:</b> <span style={{ color: "var(--text-muted)" }}>{data.most_common_challenge_type}</span></p>
    </div>
  );
}

export default BehaviorAnalytics;
