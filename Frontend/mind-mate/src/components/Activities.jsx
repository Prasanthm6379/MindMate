// src/components/Activities.jsx
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { activityAPI } from '../services/api';

export default function Activities() {
    const { user } = useAuth();
    const [activities, setActivities] = useState([]);
    const [newActivity, setNewActivity] = useState({
        activity_type: '',
        details: '',
        activity_time: new Date().toISOString(),
    });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadActivities();
    }, []);

    const loadActivities = async () => {
        setLoading(true);
        try {
            let user_id = sessionStorage.getItem('user_id');
            // console.log(user_id);
            
            const data = await activityAPI.getActivities(user_id);
            setActivities(data.data);
        } catch (error) {
            console.error('Error loading activities:', error);
        } finally {
            setLoading(false);
        }
    };

    const createActivity = async (e) => {
        e.preventDefault();
        try {
            await activityAPI.createActivity({
                ...newActivity,
                user_id: sessionStorage.getItem('user_id'),
            });
            setNewActivity({
                activity_type: '',
                details: '',
                activity_time: new Date().toISOString(),
            });
            await loadActivities();
        } catch (error) {
            console.error('Error creating activity:', error);
        }
    };

    return (
        <div className="p-4 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6 text-purple-600">Daily Activities</h1>

            <form onSubmit={createActivity} className="mb-8 bg-white p-4 rounded-lg shadow-md">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                        type="text"
                        placeholder="Activity Type (e.g., Exercise)"
                        className="p-2 border-2 border-purple-200 rounded-lg"
                        value={newActivity.activity_type}
                        onChange={(e) =>
                            setNewActivity({ ...newActivity, activity_type: e.target.value })
                        }
                        required
                    />
                    <input
                        type="datetime-local"
                        className="p-2 border-2 border-purple-200 rounded-lg"
                        value={newActivity.activity_time}
                        onChange={(e) =>
                            setNewActivity({ ...newActivity, activity_time: e.target.value })
                        }
                        required
                    />
                    <textarea
                        placeholder="Details (e.g., 100 Push-ups)"
                        className="p-2 border-2 border-purple-200 rounded-lg"
                        value={newActivity.details}
                        onChange={(e) =>
                            setNewActivity({ ...newActivity, details: e.target.value })
                        }
                        required
                    />
                </div>
                <button
                    type="submit"
                    className="mt-4 bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700"
                >
                    Log Activity
                </button>
            </form>

            {loading ? (
                <div className="text-center text-gray-600">Loading activities...</div>
            ) : (
                <div className="space-y-4">
                    {activities.map((activity) => (
                        <div
                            key={activity.id}
                            className="bg-purple-100 p-4 rounded-lg shadow-md"
                        >
                            <div className="flex justify-between items-center">
                                <div>
                                    <h3 className="text-xl font-bold">{activity.activity_type}</h3>
                                    <p className="text-gray-600">{activity.details}</p>
                                    <p className="text-blue-600">
                                        {new Date(activity.activity_time).toLocaleString()}
                                    </p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}