// src/components/Reminders.jsx
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { reminderAPI } from '../services/api';

export default function Reminders() {
    const { user } = useAuth();
    const [reminders, setReminders] = useState([]);
    const [newReminder, setNewReminder] = useState({
        title: '',
        description: '',
        reminder_time: '',
        repeat_interval: 'daily'
    });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadReminders();
    }, []);

    const loadReminders = async () => {
        setLoading(true);
        try {
            const data = await reminderAPI.getReminders(sessionStorage.getItem("user_id"));
            console.log(data);
            
            setReminders(data);
        } catch (error) {
            console.error('Error loading reminders:', error);
        } finally {
            setLoading(false);
        }
    };

    const createReminder = async (e) => {
        e.preventDefault();
        try {
            await reminderAPI.createReminder({
                ...newReminder,
                user_id: sessionStorage.getItem('user_id')
            });
            setNewReminder({
                title: '',
                description: '',
                reminder_time: '',
                repeat_interval: 'daily'
            });
            await loadReminders();
        } catch (error) {
            console.error('Error creating reminder:', error);
        }
    };

    return (
        <div className="p-4 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6 text-green-600">Reminders</h1>

            <form onSubmit={createReminder} className="mb-8 bg-white p-4 rounded-lg shadow-md">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                        type="text"
                        placeholder="Title"
                        className="p-2 border-2 border-green-200 rounded-lg"
                        value={newReminder.title}
                        onChange={(e) => setNewReminder({ ...newReminder, title: e.target.value })}
                        required
                    />
                    <input
                        type="datetime-local"
                        className="p-2 border-2 border-green-200 rounded-lg"
                        value={newReminder.reminder_time}
                        onChange={(e) => setNewReminder({ ...newReminder, reminder_time: e.target.value })}
                        required
                    />
                    <select
                        className="p-2 border-2 border-green-200 rounded-lg"
                        value={newReminder.repeat_interval}
                        onChange={(e) => setNewReminder({ ...newReminder, repeat_interval: e.target.value })}
                    >
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                    </select>
                    <textarea
                        placeholder="Description"
                        className="p-2 border-2 border-green-200 rounded-lg"
                        value={newReminder.description}
                        onChange={(e) => setNewReminder({ ...newReminder, description: e.target.value })}
                    />
                </div>
                <button
                    type="submit"
                    className="mt-4 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700"
                >
                    Add Reminder
                </button>
            </form>

            {loading ? (
                <div className="text-center text-gray-600">Loading reminders...</div>
            ) : (
                <div className="space-y-4">
                    {reminders.map(reminder => (
                        <div key={reminder.id} className="bg-green-100 p-4 rounded-lg shadow-md">
                            <div className="flex items-center justify-between">
                                <div>
                                    <h3 className="text-xl font-bold">{reminder.title}</h3>
                                    <p className="text-gray-600">{reminder.description}</p>
                                    <p className="text-blue-600">
                                        {new Date(reminder.reminder_time).toLocaleString()}
                                    </p>
                                    <p>Repeats: {reminder.repeat_interval}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}