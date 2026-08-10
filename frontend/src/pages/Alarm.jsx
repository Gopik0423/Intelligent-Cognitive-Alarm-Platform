import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../services/api";

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
    <div
      className="app-card"
      style={{
        width: "700px",
        margin: "40px auto",
        padding: "28px",
      }}
    >
      <h2>Alarm Management</h2>

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

        <button onClick={createAlarm} className="app-btn" style={{ alignSelf: "flex-start", padding: "11px 24px" }}>
          Add Alarm
        </button>
      </div>

      <hr style={{ border: "none", borderTop: "1px solid var(--border)", margin: "28px 0" }} />

      <h3>Saved Alarms</h3>

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
          <h4 style={{ marginBottom: "10px" }}>{alarm.label}</h4>
          <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}>Time : {alarm.alarm_time}</p>
          <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}>Type : {alarm.alarm_type}</p>
          <p style={{ color: "var(--text-muted)", marginBottom: "4px" }}>Challenge : {alarm.challenge_type}</p>
          <p style={{ color: "var(--text-muted)", marginBottom: "12px" }}>Status : {alarm.is_active ? "Enabled" : "Disabled"}</p>

          <div style={{ display: "flex", gap: "10px" }}>
            <button onClick={() => toggleAlarm(alarm.id)} className="app-btn-secondary" style={{ borderRadius: "8px", padding: "9px 16px", cursor: "pointer", fontWeight: 600 }}>
              Toggle
            </button>

            <button
              onClick={() => deleteAlarm(alarm.id)}
              className="app-btn-danger"
              style={{ borderRadius: "8px", padding: "9px 16px", cursor: "pointer", fontWeight: 600 }}
            >
              Delete
            </button>

            <Link to={`/verify/${alarm.id}`}>
              <button className="app-btn" style={{ padding: "9px 16px" }}>
                Test Wake-Up Verification
              </button>
            </Link>
          </div>
        </div>
      ))}
    </div>
  );
}

export default Alarm;
