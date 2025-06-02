// components/Navigation.jsx
import { Link } from 'react-router-dom';

export default function Navigation() {
    return (
        <nav className="fixed bottom-0 w-full bg-blue-600 p-4">
            <div className="flex justify-around text-white">
                <Link to="/dashboard" className="p-2 hover:bg-blue-700 rounded-lg">
                    🏠 Home
                </Link>
                <Link to="/dashboard/alerts" className="p-2 hover:bg-blue-700 rounded-lg">
                    🚨 Alerts
                </Link>
                <Link to="/dashboard/activities" className="p-2 hover:bg-blue-700 rounded-lg">
                    📝 Activities
                </Link>
                <Link to="/dashboard/reminders" className="p-2 hover:bg-blue-700 rounded-lg">
                    ⏰ Reminders
                </Link>
                <Link to="/dashboard/caregivers" className="p-2 hover:bg-blue-700 rounded-lg">
                    👪 Caregivers
                </Link>
            </div>
        </nav>
    );
}