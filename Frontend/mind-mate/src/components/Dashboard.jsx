// src/components/Dashboard.jsx
import { Outlet } from 'react-router-dom';
import { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
    const { initialize } = useAuth();

    // Initialize auth state on mount
    useEffect(() => {
        initialize();
    }, [initialize]);

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <Outlet /> {/* This renders the nested routes */}
            </div>
        </div>
    );
}