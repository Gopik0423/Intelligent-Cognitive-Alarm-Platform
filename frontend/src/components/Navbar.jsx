import { Link, useNavigate } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import "./Navbar.css";
function Navbar() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="logo">
        <h2>Cognitive Alarm</h2>
      </div>

      <div className="menu">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/alarm">Alarm</Link>
        <Link to="/challenge">Challenge</Link>
        <Link to="/sleep">Sleep</Link>
        <Link to="/habit">Habit</Link>
        <Link to="/difficulty">Difficulty</Link>
        <Link to="/recommendation">Recommendations</Link>
        <Link to="/behavior">Behavior</Link>
        <Link to="/reports">Reports</Link>
        <Link to="/profile">Profile</Link>

        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === "light" ? "🌙 Dark" : "☀️ Light"}
        </button>

        <button className="app-btn-secondary" style={{ borderRadius: "8px", padding: "8px 18px", fontWeight: 600, cursor: "pointer" }} onClick={logout}>
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
