import { NavLink, useNavigate } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import {
  LayoutDashboard,
  AlarmClock,
  Puzzle,
  Moon,
  Heart,
  Zap,
  Sparkles,
  TrendingUp,
  FileText,
  User,
} from "lucide-react";

const links = [
  { to: "/dashboard", label: "Dashboard", Icon: LayoutDashboard },
  { to: "/alarm", label: "Alarm", Icon: AlarmClock },
  { to: "/challenge", label: "Challenge", Icon: Puzzle },
  { to: "/sleep", label: "Sleep", Icon: Moon },
  { to: "/habit", label: "Habit", Icon: Heart },
  { to: "/difficulty", label: "Difficulty", Icon: Zap },
  { to: "/recommendation", label: "Recommendations", Icon: Sparkles },
  { to: "/behavior", label: "Behavior", Icon: TrendingUp },
  { to: "/reports", label: "Reports", Icon: FileText },
  { to: "/profile", label: "Profile", Icon: User },
];

function Navbar() {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-mark"><Sparkles size={18} /></div>
        <div className="sidebar-logo">Cognitive Alarm<span>SMART WAKEUP</span></div>
      </div>

      <nav className="sidebar-links">
        {links.map(({ to, label, Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) => "sidebar-link" + (isActive ? " active" : "")}
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === "light" ? "🌙 Dark" : "☀️ Light"}
        </button>

        <button
          className="app-btn-secondary"
          style={{ borderRadius: "8px", padding: "10px 12px", fontWeight: 600, cursor: "pointer" }}
          onClick={logout}
        >
          Logout
        </button>
      </div>
    </aside>
  );
}

export default Navbar;
