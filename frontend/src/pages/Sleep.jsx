import { useEffect, useState } from "react";
import API from "../services/api";

function Sleep() {
  const [sleep, setSleep] = useState({ sleep_time: "", wake_time: "" });
  const [exists, setExists] = useState(false);

  useEffect(() => {
    getSleep();
  }, []);

  const getSleep = async () => {
    try {
      const res = await API.get("/sleep/");
      setSleep({
        sleep_time: res.data.sleep_time?.slice(0, 5) || "",
        wake_time: res.data.wake_time?.slice(0, 5) || "",
      });
      setExists(true);
    } catch (err) {
      console.log(err.response?.data || err.message);
      setExists(false);
    }
  };

  const handleChange = (e) => {
    setSleep({ ...sleep, [e.target.name]: e.target.value });
  };

  const saveSleep = async () => {
    const payload = {
      sleep_time: sleep.sleep_time + ":00",
      wake_time: sleep.wake_time + ":00",
    };

    try {
      if (exists) {
        await API.put("/sleep/", payload);
      } else {
        await API.post("/sleep/", payload);
        setExists(true);
      }
      alert("Sleep Schedule Saved");
    } catch (err) {
      console.log(err.response?.data || err.message);
      alert("Save Failed");
    }
  };

  return (
    <div
      className="app-card"
      style={{
        width: "500px",
        margin: "40px auto",
        padding: "28px",
      }}
    >
      <h2>Sleep Schedule</h2>

      <div style={{ display: "flex", flexDirection: "column", gap: "14px", marginTop: "16px" }}>
        <div>
          <label style={{ fontSize: "13px", color: "var(--text-muted)" }}>Sleep Time</label>
          <input
            type="time"
            name="sleep_time"
            value={sleep.sleep_time}
            onChange={handleChange}
            className="app-input"
            style={{ marginTop: "6px" }}
          />
        </div>

        <div>
          <label style={{ fontSize: "13px", color: "var(--text-muted)" }}>Wake Time</label>
          <input
            type="time"
            name="wake_time"
            value={sleep.wake_time}
            onChange={handleChange}
            className="app-input"
            style={{ marginTop: "6px" }}
          />
        </div>

        <button onClick={saveSleep} className="app-btn" style={{ alignSelf: "flex-start", padding: "11px 24px" }}>
          {exists ? "Update Schedule" : "Save Schedule"}
        </button>
      </div>
    </div>
  );
}

export default Sleep;
