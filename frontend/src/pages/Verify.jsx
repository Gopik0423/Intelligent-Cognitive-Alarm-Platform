import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../services/api";

function Verify() {
  const { alarmId } = useParams();
  const navigate = useNavigate();

  const [verificationId, setVerificationId] = useState(null);
  const [question, setQuestion] = useState("");
  const [attempts, setAttempts] = useState(0);
  const [maxAttempts, setMaxAttempts] = useState(3);
  const [answer, setAnswer] = useState("");
  const [status, setStatus] = useState("idle");
  const [feedback, setFeedback] = useState("");

  const startVerification = async () => {
    try {
      const res = await API.post(`/verification/start/${alarmId}`);
      setVerificationId(res.data.verification_id);
      setQuestion(res.data.question);
      setAttempts(res.data.attempts);
      setMaxAttempts(res.data.max_attempts);
      setStatus("pending");
      setFeedback("");
      setAnswer("");
    } catch (err) {
      console.log(err.response?.data || err.message);
      alert("Could not start verification");
    }
  };

  const submitAnswer = async () => {
    if (!verificationId) return;

    try {
      const res = await API.post(
        `/verification/${verificationId}/submit?answer=${encodeURIComponent(answer)}`
      );

      const data = res.data;

      if (data.status === "success") {
        setStatus("success");
        setFeedback(data.message);
      } else if (data.status === "failed") {
        setStatus("failed");
        setFeedback(data.message);
      } else if (data.status === "timed_out") {
        setStatus("timed_out");
        setFeedback(data.message);
      } else if (data.status === "pending") {
        setQuestion(data.next_question);
        setAttempts((a) => a + 1);
        setFeedback(data.correct ? "Correct! One more to confirm you're awake." : "Not quite -- try this one.");
        setAnswer("");
      }
    } catch (err) {
      console.log(err.response?.data || err.message);
      alert("Submission failed");
    }
  };

  return (
    <div
      className="app-card"
      style={{
        width: "500px",
        margin: "60px auto",
        padding: "32px",
        textAlign: "center",
      }}
    >
      <h2>Wake-Up Verification</h2>
      <p style={{ color: "var(--text-muted)" }}>Simulating alarm #{alarmId} ringing right now</p>

      {status === "idle" && (
        <button
          onClick={startVerification}
          className="app-btn"
          style={{ padding: "12px 24px", fontSize: "15px" }}
        >
          Alarm Ringing -- Solve to Dismiss
        </button>
      )}

      {status === "pending" && (
        <div>
          <p style={{ fontSize: "13px", color: "var(--text-muted)" }}>
            Attempt {attempts} / {maxAttempts}
          </p>

          {feedback && <p style={{ color: "var(--primary)" }}>{feedback}</p>}

          <h1 style={{ margin: "20px 0" }}>{question}</h1>

          <input
            type="text"
            placeholder="Your answer"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            className="app-input"
            style={{ fontSize: "16px", marginBottom: "16px" }}
          />

          <button
            onClick={submitAnswer}
            className="app-btn"
            style={{ width: "100%", padding: "12px", fontSize: "16px" }}
          >
            Submit Answer
          </button>
        </div>
      )}

      {status === "success" && (
        <div>
          <h1 style={{ color: "var(--success)" }}>Verified!</h1>
          <p style={{ color: "var(--text-muted)" }}>{feedback}</p>
          <button onClick={() => navigate("/alarm")} className="app-btn-secondary" style={{ borderRadius: "8px", padding: "10px 18px", fontWeight: 600, cursor: "pointer" }}>
            Back to Alarms
          </button>
        </div>
      )}

      {(status === "failed" || status === "timed_out") && (
        <div>
          <h1 style={{ color: "var(--danger)" }}>{status === "failed" ? "Verification Failed" : "Time's Up"}</h1>
          <p style={{ color: "var(--text-muted)" }}>{feedback}</p>
          <div style={{ display: "flex", gap: "10px", justifyContent: "center" }}>
            <button onClick={startVerification} className="app-btn">Try Again</button>
            <button onClick={() => navigate("/alarm")} className="app-btn-secondary" style={{ borderRadius: "8px", padding: "11px 20px", fontWeight: 600, cursor: "pointer" }}>
              Back to Alarms
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Verify;
