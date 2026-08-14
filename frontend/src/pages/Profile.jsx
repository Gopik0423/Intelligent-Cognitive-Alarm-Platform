import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import { Brain, ChevronRight, ShieldCheck, Sparkles } from "lucide-react";

function Profile() {
  const [profile, setProfile] = useState({
    full_name: "",
    age: "",
    gender: "",
    timezone: "",
  });

  const [exists, setExists] = useState(false);
  const [account, setAccount] = useState({});
  const [intelligence, setIntelligence] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    getProfile();
  }, []);

  const getProfile = async () => {
    try {
      const userRes = await API.get("/user");
      setAccount(userRes.data);
    } catch (err) {
      console.log("Account details unavailable:", err.response?.data || err.message);
    }
    try {
      const res = await API.get("/profile/");
      setProfile(res.data);
      setExists(true);
    } catch (err) {
      console.log(err.response?.data || err.message);
      setExists(false);
    }

    // Intelligence remains useful even before the optional profile form is saved.
    try {
      const userRes = await API.get("/user");
      const intelligenceRes = await API.get(`/recommendation/${userRes.data.id}/alarm-intelligence`);
      setIntelligence(intelligenceRes.data);
    } catch (err) {
      console.log("Intelligence status unavailable:", err.response?.data || err.message);
    }
  };

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const saveProfile = async () => {
    const payload = {
      full_name: account.name || profile.full_name,
      age: Number(account.age || profile.age),
      gender: profile.gender,
      timezone: profile.timezone,
    };

    try {
      if (exists) {
        await API.put("/profile/", payload);
      } else {
        await API.post("/profile/", payload);
        setExists(true);
      }
      alert("Profile Saved Successfully");
    } catch (err) {
      console.log(err.response?.data || err.message);
      alert("Save Failed");
    }
  };

  return (
    <div style={{ width: "620px", margin: "40px auto" }}>
      <div className="app-card" style={{ padding: "28px" }}>
      <h2>User Profile</h2>
      <p style={{ marginTop: "-4px", color: "var(--text-muted)", fontSize: "14px" }}>Your name and age were saved when you created your account. Add or update your preferences here.</p>

      <div className="account-summary">
        <span><b>Name</b>{account.name || profile.full_name || "—"}</span>
        <span><b>Age</b>{account.age || profile.age || "—"}</span>
        <span><b>Date of birth</b>{account.date_of_birth || "—"}</span>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "14px", marginTop: "16px" }}>
        <select
          name="gender"
          value={profile.gender}
          onChange={handleChange}
          className="app-input"
        >
          <option value="">Gender</option><option value="Female">Female</option><option value="Male">Male</option><option value="Non-binary">Non-binary</option><option value="Prefer not to say">Prefer not to say</option>
        </select>

        <input
          type="text"
          name="timezone"
          placeholder="Timezone (e.g. Asia/Kolkata)"
          value={profile.timezone}
          onChange={handleChange}
          className="app-input"
        />

        <button onClick={saveProfile} className="app-btn" style={{ alignSelf: "flex-start", padding: "11px 24px" }}>
          {exists ? "Update Profile" : "Create Profile"}
        </button>
      </div>
      </div>

      <div className="profile-intelligence-card">
        <div className="profile-intelligence-icon"><Brain size={22} /></div>
        <div style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: "7px" }}>
            <h3>Adaptive Alarm Profile</h3>
            {intelligence?.validated && <span className="profile-verified"><ShieldCheck size={13} /> Active</span>}
          </div>
          <p>
            Your current challenge level is <b>{intelligence?.current_difficulty || "being prepared"}</b>.
            {intelligence?.behavior?.records_analyzed
              ? ` Based on ${intelligence.behavior.records_analyzed} recent attempts.`
              : " Complete challenges to build your personalized behavior profile."}
          </p>
          <div className="profile-intelligence-actions">
            <button className="profile-link-btn" onClick={() => navigate("/difficulty")}>View difficulty <ChevronRight size={16} /></button>
            <button className="profile-link-btn" onClick={() => navigate("/recommendation")}><Sparkles size={15} /> View guidance</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
