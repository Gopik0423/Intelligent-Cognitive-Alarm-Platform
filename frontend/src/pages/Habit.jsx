import { useEffect, useState } from "react";
import API from "../services/api";

function Habit() {
  const [habit, setHabit] = useState({ habit_name: "", productivity_type: "exercise" });
  const [exists, setExists] = useState(false);

  useEffect(() => {
    getHabit();
  }, []);

  const getHabit = async () => {
    try {
      const res = await API.get("/habit/");
      setHabit(res.data);
      setExists(true);
    } catch (err) {
      console.log(err.response?.data || err.message);
      setExists(false);
    }
  };

  const handleChange = (e) => {
    setHabit({ ...habit, [e.target.name]: e.target.value });
  };

  const saveHabit = async () => {
    try {
      if (exists) {
        await API.put("/habit/", habit);
      } else {
        await API.post("/habit/", habit);
        setExists(true);
      }
      alert("Habit Saved");
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
      <h2>Your Habit</h2>

      <div style={{ display: "flex", flexDirection: "column", gap: "14px", marginTop: "16px" }}>
        <input
          type="text"
          name="habit_name"
          placeholder="e.g. Morning workout"
          value={habit.habit_name}
          onChange={handleChange}
          className="app-input"
        />

        <select
          name="productivity_type"
          value={habit.productivity_type}
          onChange={handleChange}
          className="app-input"
        >
          <option value="exercise">Exercise</option>
          <option value="study">Study</option>
          <option value="mindfulness">Mindfulness</option>
          <option value="other">Other</option>
        </select>

        <button onClick={saveHabit} className="app-btn" style={{ alignSelf: "flex-start", padding: "11px 24px" }}>
          {exists ? "Update Habit" : "Save Habit"}
        </button>
      </div>
    </div>
  );
}

export default Habit;
