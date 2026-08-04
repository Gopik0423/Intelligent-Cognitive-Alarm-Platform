import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    setError("");

    if (!username || !password) {
      setError("Please enter username and password.");
      return;
    }

    setLoading(true);

    try {
      // FastAPI OAuth2 expects x-www-form-urlencoded
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await API.post("/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

localStorage.setItem(
 "token",
 response.data.access_token
);

const user = await API.get("/user");

localStorage.setItem(
  "user",
  JSON.stringify(user.data)
);
      alert("Login Successful");

      navigate("/dashboard");
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
    <div
      style={{
        width: "400px",
        margin: "60px auto",
        padding: "30px",
        borderRadius: "10px",
        background: "#ffffff",
        boxShadow: "0px 0px 10px lightgray",
      }}
    >
      <h2 style={{ textAlign: "center" }}>
        Intelligent Cognitive Alarm Platform
      </h2>

      <h3 style={{ textAlign: "center" }}>Login</h3>

      <form onSubmit={handleLogin}>

        <label>Email</label>

        <input
          type="text"
          placeholder="Enter Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            marginBottom: "15px",
          }}
        />

        <label>Password</label>

        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "5px",
            marginBottom: "20px",
          }}
        />

        {error && (
          <p style={{ color: "red" }}>
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            width: "100%",
            padding: "12px",
            background: "#1e3a8a",
            color: "white",
            border: "none",
            cursor: "pointer",
            fontSize: "16px",
          }}
        >
          {loading ? "Logging in..." : "Login"}
        </button>

      </form>

      <br />

      <p style={{ textAlign: "center" }}>
        Don't have an account?{" "}
        <Link to="/signup">
          Register
        </Link>
      </p>

    </div>
  );
}

export default Login;