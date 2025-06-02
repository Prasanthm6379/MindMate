// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Navigation from './components/Navigation';
import MemoryNotes from './components/MemoryNotes';
import EmergencyAlerts from './components/EmergencyAlerts';
import Activities from './components/Activities';
import Reminders from './components/Reminders';
import Caregivers from './components/Caregivers';

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-gray-50 pb-20">
                <Dashboard />
                <Navigation />
              </div>
            </ProtectedRoute>
          }
        >
          <Route index element={<MemoryNotes />} />
          <Route path="alerts" element={<EmergencyAlerts />} />
          <Route path="activities" element={<Activities />} />
          <Route path="reminders" element={<Reminders />} />
          <Route path="caregivers" element={<Caregivers />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}