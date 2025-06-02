// src/components/EmergencyAlerts.jsx
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { caregiverAPI, emergencyAPI } from '../services/api';

export default function EmergencyAlerts() {
    const { user } = useAuth();
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [caregivers, setCaregivers] = useState([])

    useEffect(() => {
        loadAlerts();
    }, []);

    const loadAlerts = async () => {
        setLoading(true);
        try {
            const data = await emergencyAPI.getAlerts(sessionStorage.getItem('user_id'));
            setAlerts(data.data);
        } catch (error) {
            console.error('Error loading alerts:', error);
        } finally {
            setLoading(false);
        }
    };

    const triggerAlert = async () => {
        if (!window.confirm('Are you sure you want to trigger an emergency alert?')) return;
    
        try {
            // Step 1: Get the user's current location
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, {
                    enableHighAccuracy: true,
                    timeout: 10000,
                });
            });
    
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };
    
            // Step 2: Fetch caregivers
            const data = await caregiverAPI.getCaregivers(sessionStorage.getItem('user_id'));
            setCaregivers(data.data);
    
            // Step 3: Send alerts with location
            await Promise.all(
                data.data.map((caregiver) =>
                    emergencyAPI.createAlert({
                        user_id: sessionStorage.getItem('user_id'),
                        caregiver_id: caregiver.id,
                        alert_time: new Date().toISOString(),
                        location: userLocation, // Now includes real coordinates
                        resolved: false,
                    })
                )
            );
    
            await loadAlerts();
        } catch (error) {
            console.error('Error triggering alert:', error);
            if (error.code === error.PERMISSION_DENIED) {
                alert("Location access was denied. Alerts will not include precise location.");
            }
        }
    };

    return (
        <div className="p-4 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6 text-red-600">Emergency Alerts</h1>

            <div className="text-center mb-8">
                <button
                    onClick={triggerAlert}
                    className="bg-red-600 text-white text-2xl px-8 py-6 rounded-full 
                   hover:bg-red-700 shadow-lg animate-pulse"
                >
                    🚨 EMERGENCY HELP 🚨
                </button>
                <p className="mt-4 text-gray-600 text-lg">
                    Press this button to alert your caregivers immediately
                </p>
            </div>

            {loading ? (
                <div className="text-center text-gray-600">Loading alerts...</div>
            ) : (
                <div className="space-y-4">
                    {alerts.map(alert => (
                        <div key={alert.id} className="bg-red-100 p-4 rounded-lg shadow-md">
                            <div className="flex justify-between items-center">
                                <div>
                                    <p className="font-bold">{new Date(alert.alert_time).toLocaleString()}</p>
                                    <p>Location: {alert.location}</p>
                                    <p>Status: {alert.resolved ? 'Resolved' : 'Active'}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}