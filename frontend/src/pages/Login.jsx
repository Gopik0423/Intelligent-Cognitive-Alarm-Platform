import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../services/api";
import { useTheme } from "../context/ThemeContext";
import { AlarmClock, ArrowRight, BrainCircuit, ShieldCheck } from "lucide-react";

function Login() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (event) => {
    event.preventDefault();
    if (!email || !password) return setError("Please enter your email and password.");
    setError(""); setLoading(true);
    try {
      const data = new URLSearchParams({ username: email, password });
      const response = await API.post("/login", data, { headers: { "Content-Type": "application/x-www-form-urlencoded" } });
      if (!response.data.access_token) throw new Error("Invalid login response");
      localStorage.setItem("token", response.data.access_token);
      navigate("/dashboard");
      // Enter as soon as FastAPI has authenticated the user.  Loading the
      // optional cached user record must not prevent a successful sign-in.
      API.get("/user")
        .then((user) => localStorage.setItem("user", JSON.stringify(user.data)))
        .catch(() => localStorage.removeItem("user"));
    } catch (err) {
      const serverMessage = err.response?.data?.detail || err.response?.data?.message;
      setError(serverMessage === "User not found" ? "No account exists for this email. Please create an account first." : serverMessage || "Invalid email or password.");
    } finally { setLoading(false); }
  };

  return <div className="auth-page">
    <button className="theme-toggle auth-theme-toggle" onClick={toggleTheme}>{theme === "light" ? "🌙 Dark" : "☀️ Light"}</button>
    <main className="auth-layout">
      <section className="auth-intro">
        <div className="auth-logo"><AlarmClock size={23} /></div>
        <p className="auth-kicker">COGNITIVE ALARM</p>
        <h1>Wake with purpose.</h1>
        <p>Build a better morning with adaptive challenges that learn from your progress.</p>
        <div className="auth-benefits"><span><BrainCircuit size={17} /> Adapts to your performance</span><span><ShieldCheck size={17} /> Smarter, verified wake-ups</span></div>
      </section>
      <section className="auth-card app-card">
        <p className="auth-kicker">WELCOME BACK</p>
        <h2>Sign in to your routine</h2>
        <p className="auth-subtitle">Continue building a more focused morning.</p>
        <form onSubmit={handleLogin}>
          <label className="auth-label">Email</label>
          <input type="email" placeholder="name@example.com" value={email} onChange={(e) => setEmail(e.target.value)} className="app-input auth-input" autoComplete="email" />
          <label className="auth-label">Password</label>
          <input type="password" placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)} className="app-input auth-input" autoComplete="current-password" />
          {error && <p className="auth-error">{error}</p>}
          <button type="submit" disabled={loading} className="app-btn auth-submit">{loading ? "Signing in..." : <>Sign in <ArrowRight size={17} /></>}</button>
        </form>
        <p className="auth-footer">Don't have an account? <Link to="/signup">Create account</Link></p>
      </section>
    </main>
  </div>;
}
export default Login;
