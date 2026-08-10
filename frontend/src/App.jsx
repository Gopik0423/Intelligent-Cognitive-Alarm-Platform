import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import AlarmWatcher from "./components/AlarmWatcher";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Alarm from "./pages/Alarm";
import Profile from "./pages/Profile";
import Challenge from "./pages/Challenge";
import Sleep from "./pages/Sleep";
import Habit from "./pages/Habit";
import Difficulty from "./pages/Difficulty";
import Recommendation from "./pages/Recommendation";
import BehaviorAnalytics from "./pages/BehaviorAnalytics";
import Reports from "./pages/Reports";
import Verify from "./pages/Verify";

function withNav(element, token) {
  return token ? (
    <div className="app-layout">
      <Navbar />
      <div className="main-content">
        {element}
      </div>
      <AlarmWatcher />
    </div>
  ) : (
    <Navigate to="/" />
  );
}

function App() {

  const token = localStorage.getItem("token");

  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/dashboard" element={withNav(<Dashboard />, token)} />
      <Route path="/alarm" element={withNav(<Alarm />, token)} />
      <Route path="/challenge" element={withNav(<Challenge />, token)} />
      <Route path="/profile" element={withNav(<Profile />, token)} />
      <Route path="/sleep" element={withNav(<Sleep />, token)} />
      <Route path="/habit" element={withNav(<Habit />, token)} />
      <Route path="/difficulty" element={withNav(<Difficulty />, token)} />
      <Route path="/recommendation" element={withNav(<Recommendation />, token)} />
      <Route path="/behavior" element={withNav(<BehaviorAnalytics />, token)} />
      <Route path="/reports" element={withNav(<Reports />, token)} />
      <Route path="/verify/:alarmId" element={token ? <Verify /> : <Navigate to="/" />} />
    </Routes>
  );
}

export default App;
