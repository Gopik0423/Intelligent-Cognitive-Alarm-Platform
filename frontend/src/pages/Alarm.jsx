import { useEffect, useState } from "react";
import API from "../services/api";

function Alarm() {

  const token = localStorage.getItem("token");

  const [alarms, setAlarms] = useState([]);

  const [time, setTime] = useState("");

  const [label, setLabel] = useState("");

  useEffect(() => {
    loadAlarms();
  }, []);

  // Get Alarms
  const loadAlarms = async () => {

    try {

      const res = await API.get(
        "http://127.0.0.1:8000/alarms/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setAlarms(res.data);

    } catch (err) {
      console.log(err);
    }
  };

  // Create Alarm
  const createAlarm = async () => {

    try {

      await API.post(
        "http://127.0.0.1:8000/alarms/",
        {
          time: time,
          label: label,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setTime("");
      setLabel("");

      loadAlarms();

    } catch (err) {
      console.log(err);
    }
  };

  // Delete Alarm
  const deleteAlarm = async (id) => {

    try {

      await axios.delete(
        `http://127.0.0.1:8000/alarms/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      loadAlarms();

    } catch (err) {
      console.log(err);
    }
  };

  // Toggle Alarm
  const toggleAlarm = async (id) => {

    try {

      await axios.patch(
        `http://127.0.0.1:8000/alarms/${id}/toggle`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      loadAlarms();

    } catch (err) {
      console.log(err);
    }
  };

  return (

    <div
      style={{
        width: "700px",
        margin: "40px auto",
        background: "white",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0 0 10px gray"
      }}
    >

      <h2>Alarm Management</h2>

      <input
        type="time"
        value={time}
        onChange={(e) => setTime(e.target.value)}
      />

      <br /><br />

      <input
        type="text"
        placeholder="Alarm Label"
        value={label}
        onChange={(e) => setLabel(e.target.value)}
      />

      <br /><br />

      <button onClick={createAlarm}>
        Add Alarm
      </button>

      <hr />

      <h3>Saved Alarms</h3>

      {alarms.map((alarm) => (

        <div
          key={alarm.id}
          style={{
            border: "1px solid gray",
            padding: "15px",
            marginBottom: "15px",
            borderRadius: "8px"
          }}
        >

          <h4>{alarm.label}</h4>

          <p>Time : {alarm.time}</p>

          <p>Status : {alarm.enabled ? "Enabled" : "Disabled"}</p>

          <button
            onClick={() => toggleAlarm(alarm.id)}
          >
            Toggle
          </button>

          <button
            onClick={() => deleteAlarm(alarm.id)}
            style={{
              marginLeft: "10px",
              background: "red",
              color: "white"
            }}
          >
            Delete
          </button>

        </div>

      ))}

    </div>

  );
}

export default Alarm;