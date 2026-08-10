import { useEffect, useRef, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import API from "../services/api";

const CHECK_INTERVAL_MS = 15000; // check every 15 seconds

function todayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
}

function alreadyTriggeredToday(alarmId) {
  return localStorage.getItem(`alarm_triggered_${alarmId}`) === todayKey();
}

function markTriggeredToday(alarmId) {
  localStorage.setItem(`alarm_triggered_${alarmId}`, todayKey());
}

function currentHHMM() {
  const d = new Date();
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

// Generates a repeating beep using the Web Audio API -- no external
// audio file needed, so there's nothing that can go missing/404.
function useBeep() {
  const ctxRef = useRef(null);
  const intervalRef = useRef(null);

  const start = () => {
    if (intervalRef.current) return;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    const ctx = new AudioCtx();
    ctxRef.current = ctx;

    const beepOnce = () => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.value = 880;
      gain.gain.setValueAtTime(0.15, ctx.currentTime);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.35);
    };

    beepOnce();
    intervalRef.current = setInterval(beepOnce, 700);
  };

  const stop = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (ctxRef.current) {
      ctxRef.current.close();
      ctxRef.current = null;
    }
  };

  useEffect(() => stop, []);

  return { start, stop };
}

function AlarmWatcher() {
  const [ringingAlarm, setRingingAlarm] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const { start: startBeep, stop: stopBeep } = useBeep();

  useEffect(() => {
    const check = async () => {
      // Don't interrupt an already-active verification screen
      if (location.pathname.startsWith("/verify/")) return;
      if (ringingAlarm) return;

      try {
        const res = await API.get("/alarms/");
        const now = currentHHMM();

        const due = res.data.find((alarm) => {
          if (!alarm.is_active) return false;
          if (alreadyTriggeredToday(alarm.id)) return false;
          const alarmHHMM = (alarm.alarm_time || "").slice(0, 5);
          return alarmHHMM === now;
        });

        if (due) {
          markTriggeredToday(due.id);
          setRingingAlarm(due);
          startBeep();
        }
      } catch (err) {
        console.log("AlarmWatcher check failed:", err.response?.data || err.message);
      }
    };

    check();
    const interval = setInterval(check, CHECK_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [location.pathname, ringingAlarm]);

  const goToVerification = () => {
    stopBeep();
    const alarmId = ringingAlarm.id;
    setRingingAlarm(null);
    navigate(`/verify/${alarmId}`);
  };

  if (!ringingAlarm) return null;

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0, 0, 0, 0.75)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 9999,
      }}
    >
      <div
        className="app-card"
        style={{
          width: "380px",
          padding: "36px",
          textAlign: "center",
        }}
      >
        <h2 style={{ margin: "0 0 10px 0" }}>Alarm Ringing</h2>
        <p style={{ color: "var(--text-muted)", marginBottom: "24px" }}>
          {ringingAlarm.label || "Wake up!"} -- {ringingAlarm.alarm_time?.slice(0, 5)}
        </p>
        <button className="app-btn" style={{ width: "100%" }} onClick={goToVerification}>
          Wake Up -- Solve to Dismiss
        </button>
      </div>
    </div>
  );
}

export default AlarmWatcher;
