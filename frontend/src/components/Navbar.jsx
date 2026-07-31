import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav style={{ padding: "15px", background: "#1e3a8a" }}>
      <Link to="/" style={{ color: "white", marginRight: "20px" }}>Login</Link>
      <Link to="/signup" style={{ color: "white", marginRight: "20px" }}>Signup</Link>
      <Link to="/dashboard" style={{ color: "white", marginRight: "20px" }}>Dashboard</Link>
      <Link to="/alarm" style={{ color: "white", marginRight: "20px" }}>Alarm</Link>
      <Link to="/challenge" style={{ color: "white", marginRight: "20px" }}>Challenge</Link>
      <Link to="/profile" style={{ color: "white" }}>Profile</Link>
    </nav>
  );
}

export default Navbar;