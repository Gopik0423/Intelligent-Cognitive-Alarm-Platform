import { useState } from "react";
import API from "../services/api";

function Challenge() {

  const token = localStorage.getItem("token");

  const [challenge, setChallenge] = useState(null);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState("");

  // Start Challenge
  const startChallenge = async () => {

    try {

      const response = await API.post(
        "http://127.0.0.1:8000/challenge/start",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setChallenge(response.data);
      setResult("");

    } catch (error) {
      console.log(error);
      alert("Unable to start challenge");
    }
  };

  // Submit Answer
  const submitAnswer = async () => {

    if (!challenge) return;

    try {

      const response = await API.post(
        `http://127.0.0.1:8000/challenge/${challenge.id}/submit`,
        {
          answer: answer,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setResult(response.data.message || "Answer Submitted");

    } catch (error) {
      console.log(error);
      alert("Submission Failed");
    }
  };

  return (
    <div
      style={{
        width: "700px",
        margin: "40px auto",
        padding: "25px",
        background: "#ffffff",
        borderRadius: "10px",
        boxShadow: "0px 0px 10px gray",
      }}
    >

      <h2>Cognitive Challenge</h2>

      <button
        onClick={startChallenge}
        style={{
          padding: "10px 20px",
          background: "#1e3a8a",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Start Challenge
      </button>

      <br />
      <br />

      {challenge && (

        <div>

          <h3>{challenge.challenge_type}</h3>

          <p>
            <b>Question:</b> {challenge.question}
          </p>

          <input
            type="text"
            placeholder="Enter Answer"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            style={{
              width: "100%",
              padding: "10px",
            }}
          />

          <br />
          <br />

          <button
            onClick={submitAnswer}
            style={{
              padding: "10px 20px",
              background: "green",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Submit Answer
          </button>

        </div>

      )}

      <br />

      {result && (
        <h3 style={{ color: "blue" }}>
          {result}
        </h3>
      )}

    </div>
  );
}

export default Challenge;