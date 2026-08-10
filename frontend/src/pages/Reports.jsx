import { useEffect, useState } from "react";
import API from "../services/api";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

const TREND_ICON = {
  improving: TrendingUp,
  declining: TrendingDown,
  stable: Minus,
};

function TrendBadge({ value }) {
  const cls = TREND_ICON[value] ? value : "stable";
  const Icon = TREND_ICON[value] || Minus;
  return (
    <span className={`trend-badge ${cls}`}>
      <Icon size={13} />
      {value}
    </span>
  );
}

function Reports() {
  const [report, setReport] = useState(null);

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    try {
      const userRes = await API.get("/user");
      const res = await API.get(`/reports/${userRes.data.id}`);
      setReport(res.data);
    } catch (err) {
      console.log(err.response?.data || err.message);
    }
  };

  if (!report) {
    return (
      <div className="spinner-wrap">
        <div className="spinner" />
      </div>
    );
  }

  const sectionStyle = {
    padding: "18px",
    borderRadius: "var(--radius)",
    border: "1px solid var(--border)",
    marginBottom: "16px",
  };

  return (
    <div style={{ width: "650px", margin: "40px auto" }}>
      <h2>Full Report</h2>
      <p style={{ color: "var(--text-muted)", fontSize: "12px" }}>Generated: {report.generated_at}</p>

      <div style={{ ...sectionStyle, background: "var(--surface-alt)" }}>
        <h4>Performance Summary ({report.attempts_analyzed} attempts)</h4>
        <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}>Success rate: {report.performance_summary.success_rate}%</p>
        <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}>Average score: {report.performance_summary.average_score}</p>
        <p style={{ color: "var(--text-muted)" }}>Average completion time: {report.performance_summary.average_completion_time}s</p>
      </div>

      <div style={{ ...sectionStyle, background: "var(--accent-blue)" }}>
        <h4>Behavioral Analytics</h4>
        <p style={{ color: "var(--text-muted)", marginBottom: "8px" }}>Status: {report.behavioral_analytics.status}</p>
        {report.behavioral_analytics.status === "ok" && (
          <>
            <p style={{ marginBottom: "8px", display: "flex", alignItems: "center", gap: "8px" }}>
              <span style={{ color: "var(--text-muted)" }}>Snooze trend:</span>
              <TrendBadge value={report.behavioral_analytics.snooze_trend} />
            </p>
            <p style={{ marginBottom: "8px", display: "flex", alignItems: "center", gap: "8px" }}>
              <span style={{ color: "var(--text-muted)" }}>Accuracy trend:</span>
              <TrendBadge value={report.behavioral_analytics.accuracy_trend} />
            </p>
            <p style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <span style={{ color: "var(--text-muted)" }}>Consistency trend:</span>
              <TrendBadge value={report.behavioral_analytics.wakeup_consistency_trend} />
            </p>
          </>
        )}
      </div>

      <div style={{ ...sectionStyle, background: "var(--accent-orange)" }}>
        <h4>Current Difficulty Level</h4>
        <p style={{ color: "var(--text-muted)" }}>{report.current_difficulty_level ?? "Not set yet"}</p>
      </div>

      {report.habit_score && (
        <div style={{ ...sectionStyle, background: "var(--accent-purple)", marginBottom: 0 }}>
          <h4>Habit Score: {report.habit_score.score}</h4>
          <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}>Wake-up consistency: {report.habit_score.wake_up_consistency}</p>
          <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}>Challenge completion: {report.habit_score.challenge_completion}</p>
          <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}>Snooze reduction: {report.habit_score.snooze_reduction}</p>
          <p style={{ color: "var(--text-muted)" }}>Sleep schedule adherence: {report.habit_score.sleep_schedule_adherence}</p>
        </div>
      )}
    </div>
  );
}

export default Reports;
