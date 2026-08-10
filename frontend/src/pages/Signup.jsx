import { useState } from "react";
import API from "../services/api";
import { useNavigate, Link } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";

function Signup() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const [formData, setFormData] = useState({
  name: "",
  email: "",
  password: "",
  role: "user",
  date_of_birth: "",
});

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSignup = async (e) => {
    e.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      await API.post("/register", formData);

      alert("Registration Successful");

      navigate("/");
    } catch (err) {
      console.log(err);

      if (err.response) {
        setMessage(err.response.data.detail || "Registration Failed");
      } else {
        setMessage("Unable to connect to server");
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
          top: "50px",
          textAlign: "center",
        }}
      >
        <h2>Cognitive Alarm</h2>

        <h3 style={{ color: "var(--text-muted)", fontWeight: 500 }}>Create Account</h3>

        <form onSubmit={handleSignup}>

          <input
            type="text"
            name="name"
            placeholder="Full Name"
            value={formData.name}
            onChange={handleChange}
            required
            className="app-input"
            style={{ marginBottom: "14px" }}
          />

          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
            className="app-input"
            style={{ marginBottom: "14px" }}
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
            className="app-input"
            style={{ marginBottom: "14px" }}
          />

          <input
              type="date"
              name="date_of_birth"
              value={formData.date_of_birth}
              onChange={handleChange}
              required
              className="app-input"
              style={{ marginBottom: "14px" }}
          />

          <button
            type="submit"
            disabled={loading}
            className="app-btn"
            style={{ width: "100%", padding: "12px", fontSize: "15px" }}
          >
            {loading ? "Creating Account..." : "Signup"}
          </button>

        </form>

        <br />

        {message && (
          <p style={{ color: "var(--danger)", fontSize: "13px" }}>
            {message}
          </p>
        )}

        <p style={{ color: "var(--text-muted)", fontSize: "14px" }}>
          Already have an account?
          <Link to="/" style={{ color: "var(--primary)", fontWeight: 600 }}> Login</Link>
        </p>

      </div>
    </div>
  );
}

export default Signup;
