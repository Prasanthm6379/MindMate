// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Login from './components/Login';
import Register from './components/Register';
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
        <Route path="/register" element={<Register />} />
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
        />
        <Route
          path="/dashboard/alerts"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-gray-50 pb-20">
                <EmergencyAlerts />
                <Navigation />
              </div>
            </ProtectedRoute>
          }
        />
                <Route
          path="/dashboard/memorynotes"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-gray-50 pb-20">
                <MemoryNotes />
                <Navigation />
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard/activities"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-gray-50 pb-20">
                <Activities />
                <Navigation />
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard/reminders"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-gray-50 pb-20">
                <Reminders />
                <Navigation />
              </div>
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard/caregivers"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-gray-50 pb-20">
                <Caregivers />
                <Navigation />
              </div>
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}