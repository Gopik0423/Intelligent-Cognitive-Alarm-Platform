import { useEffect, useState } from "react";
import API from "../services/api";

function Profile() {
  const [profile, setProfile] = useState({
    full_name: "",
    age: "",
    gender: "",
    phone: "",
    sleep_time: "",
    wake_time: "",
  });

  const token = localStorage.getItem("token");

  useEffect(() => {
    getProfile();
  }, []);

  const getProfile = async () => {
    try {
      const res = await API.get("http://127.0.0.1:8000/profile/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setProfile(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const handleChange = (e) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value,
    });
  };

  const updateProfile = async () => {
    try {
      await API.put(
        "http://127.0.0.1:8000/profile/",
        profile,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert("Profile Updated Successfully");
    } catch (err) {
      console.log(err);
      alert("Update Failed");
    }
  };

  return (
    <div
      style={{
        width: "500px",
        margin: "40px auto",
        padding: "25px",
        borderRadius: "10px",
        boxShadow: "0px 0px 10px lightgray",
        background: "#fff",
      }}
    >
      <h2>User Profile</h2>

      <br />

      <input
        type="text"
        name="full_name"
        placeholder="Full Name"
        value={profile.full_name}
        onChange={handleChange}
      />

      <br />
      <br />

      <input
        type="number"
        name="age"
        placeholder="Age"
        value={profile.age}
        onChange={handleChange}
      />

      <br />
      <br />

      <input
        type="text"
        name="gender"
        placeholder="Gender"
        value={profile.gender}
        onChange={handleChange}
      />

      <br />
      <br />

      <input
        type="text"
        name="phone"
        placeholder="Phone Number"
        value={profile.phone}
        onChange={handleChange}
      />

      <br />
      <br />

      <input
        type="time"
        name="sleep_time"
        value={profile.sleep_time}
        onChange={handleChange}
      />

      <br />
      <br />

      <input
        type="time"
        name="wake_time"
        value={profile.wake_time}
        onChange={handleChange}
      />

      <br />
      <br />

      <button onClick={updateProfile}>
        Update Profile
      </button>
    </div>
  );
}

export default Profile;