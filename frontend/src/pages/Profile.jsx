import { useEffect, useState } from "react";
import API from "../services/api";

function Profile() {
  const [profile, setProfile] = useState({
    full_name: "",
    age: "",
    gender: "",
    timezone: "",
  });

  const [exists, setExists] = useState(false);

  useEffect(() => {
    getProfile();
  }, []);

  const getProfile = async () => {
    try {
      const res = await API.get("/profile/");
      setProfile(res.data);
      setExists(true);
    } catch (err) {
      console.log(err.response?.data || err.message);
      setExists(false);
    }
  };

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const saveProfile = async () => {
    const payload = {
      full_name: profile.full_name,
      age: Number(profile.age),
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
    <div
      className="app-card"
      style={{
        width: "500px",
        margin: "40px auto",
        padding: "28px",
      }}
    >
      <h2>User Profile</h2>

      <div style={{ display: "flex", flexDirection: "column", gap: "14px", marginTop: "16px" }}>
        <input
          type="text"
          name="full_name"
          placeholder="Full Name"
          value={profile.full_name}
          onChange={handleChange}
          className="app-input"
        />

        <input
          type="number"
          name="age"
          placeholder="Age"
          value={profile.age}
          onChange={handleChange}
          className="app-input"
        />

        <input
          type="text"
          name="gender"
          placeholder="Gender"
          value={profile.gender}
          onChange={handleChange}
          className="app-input"
        />

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
  );
}

export default Profile;
