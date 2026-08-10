import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../services/api";
import { useTheme } from "../context/ThemeContext";

function Login() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    setError("");

    if (!email || !password) {
      setError("Please enter email and password.");
      return;
    }

    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await API.post("/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      localStorage.setItem("token", response.data.access_token);

      const user = await API.get("/user");

      localStorage.setItem("user", JSON.stringify(user.data));

      window.location.href = "/dashboard";
    } catch (err) {
      console.log(err);

      if (err.response) {
        setError(err.response.data.detail || "Invalid Credentials");
      } else {
        setError("Unable to connect to server.");
      }
    }

    setLoading(false);
  };

  return (
    <div style={{ position: "relative", minHeight: "100vh" }}>
      <button
        className="theme-toggle"
        onClick={toggleTheme}
        style={{ position: "absolute", top: "24px", right: "24px" }}
      >
        {theme === "light" ? "🌙 Dark" : "☀️ Light"}
      </button>

      <div
        className="app-card"
        style={{
          width: "400px",
          margin: "0 auto",
          padding: "36px",
          position: "relative",
          top: "60px",
        }}
      >
        <h2 style={{ textAlign: "center", fontSize: "22px" }}>
          Intelligent Cognitive Alarm Platform
        </h2>

        <h3 style={{ textAlign: "center", color: "var(--text-muted)", fontWeight: 500 }}>Login</h3>

        <form onSubmit={handleLogin}>

          <label style={{ fontSize: "13px", color: "var(--text-muted)" }}>Email</label>

          <input
            type="text"
            placeholder="Enter Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="app-input"
            style={{
              marginTop: "6px",
              marginBottom: "16px",
            }}
          />

          <label style={{ fontSize: "13px", color: "var(--text-muted)" }}>Password</label>

          <input
            type="password"
            placeholder="Enter Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="app-input"
            style={{
              marginTop: "6px",
              marginBottom: "20px",
            }}
          />

          {error && (
            <p style={{ color: "var(--danger)", fontSize: "13px", marginBottom: "12px" }}>
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="app-btn"
            style={{
              width: "100%",
              padding: "12px",
              fontSize: "15px",
            }}
          >
            {loading ? "Logging in..." : "Login"}
          </button>

        </form>

        <br />

        <p style={{ textAlign: "center", color: "var(--text-muted)", fontSize: "14px" }}>
          Don't have an account?{" "}
          <Link to="/signup" style={{ color: "var(--primary)", fontWeight: 600 }}>
            Register
          </Link>
        </p>

      </div>
    </div>
  );
}

export default Login;
