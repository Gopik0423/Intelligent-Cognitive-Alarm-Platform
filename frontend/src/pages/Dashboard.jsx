import { useEffect, useState } from "react";
import API from "../services/api";

function Dashboard() {

  console.log("Dashboard opened");


  const [user, setUser] = useState({});
  const [habitScore, setHabitScore] = useState(0);
  const [recommendation, setRecommendation] = useState("");
  const [analytics, setAnalytics] = useState({});


  useEffect(() => {
    getDashboard();
  }, []);


  const getDashboard = async () => {

    try {

      // Get User Details
      const userRes = await API.get("/user");

      setUser(userRes.data);

      const userId = userRes.data.id;


      // Get Habit Score
      const habitRes = await API.get("/habit-score");

      setHabitScore(habitRes.data.habit_score || 0);


      // Get Recommendation
      const recRes = await API.get(`/recommendation/${userId}`);

      setRecommendation(
        recRes.data.recommendation || ""
      );


      // Get Analytics
      const analyticsRes = await API.get(
        `/analytics/${userId}`
      );

      setAnalytics(analyticsRes.data);


    } catch (err) {

      console.log(
        "Dashboard Error:",
        err.response?.data || err.message
      );

    }

  };


  return (

    <div
      style={{
        width: "80%",
        margin: "30px auto",
        fontFamily: "Arial",
      }}
    >

      <h1>CampusCare AI Dashboard</h1>

      <hr />


      <div
        style={{
          display: "flex",
          gap: "20px",
          marginTop: "20px",
        }}
      >


        <div
          style={{
            flex: 1,
            background: "#E3F2FD",
            padding: "20px",
            borderRadius: "10px",
          }}
        >

          <h3>User</h3>

          <p>
            <b>Name:</b> {user.name}
          </p>

          <p>
            <b>Role:</b> {user.role}
          </p>

          <p>
            <b>Email:</b> {user.email}
          </p>

        </div>



        <div
          style={{
            flex: 1,
            background: "#FFF3E0",
            padding: "20px",
            borderRadius: "10px",
          }}
        >

          <h3>Habit Score</h3>

          <h1>
            {habitScore}%
          </h1>

        </div>


      </div>


      <br />


      <div
        style={{
          background: "#F1F8E9",
          padding: "20px",
          borderRadius: "10px",
        }}
      >

        <h3>
          Today's Recommendation
        </h3>

        <p>
          {recommendation}
        </p>

      </div>


      <br />


      <div
        style={{
          background: "#FCE4EC",
          padding: "20px",
          borderRadius: "10px",
        }}
      >

        <h3>
          Analytics
        </h3>


        <p>
          <b>Total Challenges :</b>{" "}
          {analytics.total_challenges || 0}
        </p>


        <p>
          <b>Completed :</b>{" "}
          {analytics.completed || 0}
        </p>


        <p>
          <b>Success Rate :</b>{" "}
          {analytics.success_rate || 0}%
        </p>


      </div>


    </div>

  );

}


export default Dashboard;