import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../services/api";
import {
  AlarmClockPlus,
  AlarmClock,
  Clock,
  RefreshCw,
  Trash2,
  Play,
} from "lucide-react";

function Alarm() {

  const [alarms, setAlarms] = useState([]);

  const [alarmTime, setAlarmTime] = useState("");
  const [label, setLabel] = useState("");
  const [alarmType, setAlarmType] = useState("daily");
  const [challengeType, setChallengeType] = useState("math");

  useEffect(() => {
    loadAlarms();
  }, []);

  const loadAlarms = async () => {
    try {
      const res = await API.get("/alarms/");
      setAlarms(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const createAlarm = async () => {
    if (!alarmTime) {
      alert("Please choose a time");
      return;
    }

    try {
      await API.post("/alarms/", {
        label: label || "Alarm",
        alarm_time: alarmTime + ":00",
        alarm_type: alarmType,
        challenge_type: challengeType,
      });

      setAlarmTime("");
      setLabel("");

      loadAlarms();
    } catch (err) {
      console.log(err.response?.data || err.message);
      alert("Could not create alarm");
    }
  };

  const deleteAlarm = async (id) => {
    try {
      await API.delete(`/alarms/${id}`);
      loadAlarms();
    } catch (err) {
      console.log(err);
    }
  };

  const toggleAlarm = async (id) => {
    try {
      await API.patch(`/alarms/${id}/toggle`);
      loadAlarms();
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div style={{ width: "700px", margin: "40px auto", display: "flex", flexDirection: "column", gap: "24px" }}>

      <div className="app-card" style={{ padding: "28px" }}>
        <h2 style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <AlarmClockPlus size={22} color="var(--primary)" />
          Create New Alarm
        </h2>

        <div style={{ display: "flex", flexDirection: "column", gap: "14px", marginTop: "16px" }}>
          <input
            type="time"
            value={alarmTime}
            onChange={(e) => setAlarmTime(e.target.value)}
            className="app-input"
          />

          <input
            type="text"
            placeholder="Alarm Label"
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            className="app-input"
          />

          <div>
            <label style={{ fontSize: "13px", color: "var(--text-muted)" }}>Alarm type: </label>
            <select value={alarmType} onChange={(e) => setAlarmType(e.target.value)} className="app-input" style={{ marginTop: "6px" }}>
              <option value="daily">Daily</option>
              <option value="smart">Smart</option>
            </select>
          </div>

          <div>
            <label style={{ fontSize: "13px", color: "var(--text-muted)" }}>Challenge type: </label>
            <select value={challengeType} onChange={(e) => setChallengeType(e.target.value)} className="app-input" style={{ marginTop: "6px" }}>
              <option value="math">Math</option>
              <option value="logic">Logic</option>
              <option value="memory">Memory</option>
              <option value="word">Word</option>
              <option value="pattern">Pattern</option>
              <option value="riddle">Riddle</option>
              <option value="quiz">Quiz</option>
            </select>
          </div>

          <button onClick={createAlarm} className="app-btn" style={{ alignSelf: "flex-start", padding: "11px 24px", display: "flex", alignItems: "center", gap: "8px" }}>
            <AlarmClockPlus size={16} />
            Add Alarm
          </button>
        </div>
      </div>

      <div className="app-card" style={{ padding: "28px" }}>
        <h2 style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <AlarmClock size={22} color="var(--primary)" />
          Your Alarms
        </h2>

        {alarms.length === 0 ? (
          <div className="empty-state">
            <AlarmClock size={36} color="var(--text-muted)" />
            <p>No alarms yet -- create one above to get started.</p>
          </div>
        ) : (
          <div style={{ marginTop: "16px" }}>
            {alarms.map((alarm) => (
              <div
                key={alarm.id}
                className="app-card"
                style={{
                  padding: "16px",
                  marginBottom: "14px",
                  boxShadow: "none",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "10px" }}>
                  <h4 style={{ margin: 0 }}>{alarm.label}</h4>
                  <span className={`status-pill ${alarm.is_active ? "enabled" : "disabled"}`}>
                    {alarm.is_active ? "Enabled" : "Disabled"}
                  </span>
                </div>

                <p style={{ color: "var(--text-muted)", marginBottom: "4px", display: "flex", alignItems: "center", gap: "6px" }}>
                  <Clock size={14} /> {alarm.alarm_time}
                </p>
                <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}>Type : {alarm.alarm_type}</p>
                <p style={{ color: "var(--text-muted)", marginBottom: "12px" }}>Challenge : {alarm.challenge_type}</p>

                <div style={{ display: "flex", gap: "10px" }}>
                  <button onClick={() => toggleAlarm(alarm.id)} className="app-btn-secondary" style={{ borderRadius: "8px", padding: "9px 16px", cursor: "pointer", fontWeight: 600, display: "flex", alignItems: "center", gap: "6px" }}>
                    <RefreshCw size={14} />
                    Toggle
                  </button>

                  <button
                    onClick={() => deleteAlarm(alarm.id)}
                    className="app-btn-danger"
                    style={{ borderRadius: "8px", padding: "9px 16px", cursor: "pointer", fontWeight: 600, display: "flex", alignItems: "center", gap: "6px" }}
                  >
                    <Trash2 size={14} />
                    Delete
                  </button>

                  <Link to={`/verify/${alarm.id}`}>
                    <button className="app-btn" style={{ padding: "9px 16px", display: "flex", alignItems: "center", gap: "6px" }}>
                      <Play size={14} />
                      Test Wake-Up Verification
                    </button>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Alarm;
