import { useEffect, useState } from "react";
import API from "../services/api";
import { BrainCircuit, CheckCircle2, CircleHelp, Play, Sparkles, Trophy, XCircle } from "lucide-react";

const MAX_ATTEMPTS = 3;

function Challenge() {
  const [challenge, setChallenge] = useState(null);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [memoryVisible, setMemoryVisible] = useState(false);
  const [memorySeconds, setMemorySeconds] = useState(0);
  const [attempts, setAttempts] = useState(0);
  const isMemory = challenge?.challenge_type?.toLowerCase() === "memory";
  const attemptsLeft = MAX_ATTEMPTS - attempts;
  const finished = Boolean(result?.correct) || attempts >= MAX_ATTEMPTS;

  useEffect(() => {
    if (!isMemory || !memoryVisible) return undefined;
    const startedAt = Date.now();
    const interval = window.setInterval(() => {
      const secondsLeft = Math.max(0, Math.ceil((4000 - (Date.now() - startedAt)) / 1000));
      setMemorySeconds(secondsLeft);
      if (secondsLeft === 0) {
        window.clearInterval(interval);
        setMemoryVisible(false);
      }
    }, 100);
    return () => window.clearInterval(interval);
  }, [isMemory, memoryVisible]);

  const startChallenge = async () => {
    setMemoryVisible(false); setMemorySeconds(0); setAttempts(0); setAnswer(""); setResult(null); setLoading(true);
    try {
      const response = await API.post("/challenge/start");
      setChallenge(response.data);
      const memory = response.data.challenge_type?.toLowerCase() === "memory";
      setMemoryVisible(memory); setMemorySeconds(memory ? 4 : 0);
    } catch (error) {
      setResult({ error: error.response?.data?.detail || "Unable to start a challenge. Please try again." });
    } finally { setLoading(false); }
  };

  const submitAnswer = async () => {
    if (!challenge || !answer.trim() || finished) return;
    setLoading(true);
    try {
      const response = await API.post(`/challenge/${challenge.id}/submit`, { answer: answer.trim() });
      const nextAttempts = attempts + 1;
      setAttempts(nextAttempts);
      setAnswer("");
      setResult({ correct: response.data.correct, score: response.data.score, final: response.data.correct || nextAttempts >= MAX_ATTEMPTS });
    } catch (error) {
      setResult({ error: error.response?.data?.detail || "Submission failed. Please try again." });
    } finally { setLoading(false); }
  };

  return <div className="challenge-page">
    <header className="challenge-hero">
      <div className="challenge-icon"><BrainCircuit size={25} /></div>
      <div><p>ADAPTIVE TRAINING</p><h1>Cognitive Challenge</h1><span>Each answer helps tune your next wake-up challenge.</span></div>
      <button onClick={startChallenge} disabled={loading} className="app-btn"><Play size={16} /> {loading ? "Preparing..." : challenge ? "New challenge" : "Start challenge"}</button>
    </header>

    {challenge && <div className="challenge-card app-card">
      <div className="challenge-meta"><span><Sparkles size={15} /> {challenge.challenge_type}</span><span>Level: {challenge.difficulty}</span><span><Trophy size={15} /> {challenge.points} points</span></div>
      {isMemory && memoryVisible ? <div className="memory-preview"><span>Memorize these words · {memorySeconds}s</span><p>{challenge.question.replace(/^Remember these words:\s*/i, "")}</p></div>
        : isMemory ? <div className="memory-hidden"><BrainCircuit size={25} /><b>Words are hidden</b><span>Enter the words in the same order, separated by commas.</span></div>
        : <p className="challenge-question">{challenge.question}</p>}
      <div className="attempts-row"><span>Attempts</span>{[0, 1, 2].map((attempt) => <i key={attempt} className={attempt < attempts ? "used" : ""} />)}<b>{attemptsLeft} left</b></div>
      <label className="auth-label">Your answer</label>
      <div className="challenge-answer-row">
        <input type="text" placeholder={isMemory ? "e.g. red, sun, tree, book" : "Type your answer"} value={answer} onChange={(event) => setAnswer(event.target.value)} className="app-input" disabled={loading || memoryVisible || finished} onKeyDown={(event) => event.key === "Enter" && submitAnswer()} />
        <button onClick={submitAnswer} disabled={loading || memoryVisible || !answer.trim() || finished} className="app-btn">Submit</button>
      </div>
    </div>}

    {!challenge && !result && <div className="challenge-empty"><CircleHelp size={32} /><h3>Ready when you are</h3><p>Start a short challenge to see your adaptive level in action.</p></div>}
    {result && <div className={`challenge-result ${result.error ? "error" : result.correct ? "success" : "incorrect"}`}>
      {result.error ? <XCircle /> : result.correct ? <CheckCircle2 /> : <XCircle />}
      <div><b>{result.error ? "Something went wrong" : result.correct ? "Correct — great work!" : result.final ? "No attempts left for this challenge." : "Not quite — try again."}</b>
      <p>{result.error || (result.correct ? `You earned ${result.score} points. Start another challenge to continue your streak.` : result.final ? "Start a new challenge when you are ready." : `${attemptsLeft} attempt${attemptsLeft === 1 ? "" : "s"} remaining. The same question is still active.`)}</p></div>
    </div>}
  </div>;
}
export default Challenge;
