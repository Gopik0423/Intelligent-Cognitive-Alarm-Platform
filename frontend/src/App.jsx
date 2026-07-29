import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginSignup from './pages/LoginSignup';
import ProfileCreation from './pages/ProfileCreation';
import DashboardLayout from './components/DashboardLayout';
import UserDashboard from './pages/UserDashboard';
import WellnessDashboard from './pages/WellnessDashboard';
import AdminDashboard from './pages/AdminDashboard';
import AlarmManagement from './pages/AlarmManagement';
import NotificationSettings from './pages/NotificationSettings';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/auth" />} />
        <Route path="/auth" element={<LoginSignup />} />
        <Route path="/profile-setup" element={<ProfileCreation />} />
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<UserDashboard />} />
          <Route path="coach" element={<WellnessDashboard />} />
          <Route path="admin" element={<AdminDashboard />} />
          <Route path="alarms" element={<AlarmManagement />} />
          <Route path="notifications" element={<NotificationSettings />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
