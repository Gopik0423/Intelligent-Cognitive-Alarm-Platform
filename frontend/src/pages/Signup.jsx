import { useState } from "react";
import API from "../services/api";
import { useNavigate, Link } from "react-router-dom";

function Signup() {
  const navigate = useNavigate();

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
    <div
      style={{
        width: "400px",
        margin: "50px auto",
        padding: "30px",
        background: "#ffffff",
        borderRadius: "10px",
        boxShadow: "0px 0px 10px gray",
        textAlign: "center",
      }}
    >
      <h2>CampusCare AI</h2>

      <h3>Create Account</h3>

      <form onSubmit={handleSignup}>

        <input
          type="text"
          name="name"
          placeholder="Full Name"
          value={formData.name}
          onChange={handleChange}

          required
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "15px",
          }}
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "15px",
          }}
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "15px",
          }}
        />

        <input
            type="date"
            name="date_of_birth"
            value={formData.date_of_birth}
            onChange={handleChange}
            required
            style={{
            width: "100%",
            padding: "10px",
            marginBottom: "15px",
          }}
        />

        <select
          name="role"
          value={formData.role}
          onChange={handleChange}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "20px",
          }}
        >
          <option value="user">User</option>
          <option value="coach">Coach</option>
          <option value="admin">Admin</option>
        </select>

        <button
          type="submit"
          disabled={loading}
          style={{
            width: "100%",
            padding: "10px",
            background: "#1e3a8a",
            color: "white",
            border: "none",
            cursor: "pointer",
            fontSize: "16px",
          }}
        >
          {loading ? "Creating Account..." : "Signup"}
        </button>

      </form>

      <br />

      {message && (
        <p style={{ color: "red" }}>
          {message}
        </p>
      )}

      <p>
        Already have an account?
        <Link to="/"> Login</Link>
      </p>

    </div>
  );
}

export default Signup;