import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";
function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="logo">
        <h2>CampusCare AI</h2>
      </div>

      <div className="menu">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/alarm">Alarm</Link>
        <Link to="/challenge">Challenge</Link>
        <Link to="/profile">Profile</Link>

        <button className="logout-btn" onClick={logout}>
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;