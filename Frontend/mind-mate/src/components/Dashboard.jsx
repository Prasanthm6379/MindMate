// src/components/Dashboard.jsx
import { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
    const { initialize } = useAuth();

    // Initialize auth state on mount
    useEffect(() => {
        initialize();
    }, [initialize]);

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <h1 className="text-4xl font-bold text-gray-800 text-center">Dashboard Coming Soon!!</h1>
            </div>
        </div>
    );
}