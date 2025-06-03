// src/components/Caregivers.jsx
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { caregiverAPI } from '../services/api';

export default function Caregivers() {
    const { user } = useAuth();
    const [caregivers, setCaregivers] = useState([]);
    const [newCaregiver, setNewCaregiver] = useState({
        name: '',
        email: '',
        phone: '',
        relationship: '',
        emergency_contact: false,
    });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadCaregivers();
    }, []);

    const loadCaregivers = async () => {
        setLoading(true);
        try {
            const data = await caregiverAPI.getCaregivers(sessionStorage.getItem('user_id'));
            setCaregivers(data.data);
        } catch (error) {
            console.error('Error loading caregivers:', error);
        } finally {
            setLoading(false);
        }
    };

    const addCaregiver = async (e) => {
        e.preventDefault();
        try {
            await caregiverAPI.addCaregiver({
                ...newCaregiver,
                user_id: sessionStorage.getItem('user_id'),
            });
            setNewCaregiver({
                name: '',
                email: '',
                phone: '',
                relationship: '',
                emergency_contact: false,
            });
            await loadCaregivers();
        } catch (error) {
            console.error('Error adding caregiver:', error);
        }
    };

    return (
        <div className="p-4 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6 text-orange-600">Caregivers</h1>

            <form onSubmit={addCaregiver} className="mb-8 bg-white p-4 rounded-lg shadow-md">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                        type="text"
                        placeholder="Name"
                        className="p-2 border-2 border-orange-200 rounded-lg"
                        value={newCaregiver.name}
                        onChange={(e) =>
                            setNewCaregiver({ ...newCaregiver, name: e.target.value })
                        }
                        required
                    />
                    <input
                        type="email"
                        placeholder="Email"
                        className="p-2 border-2 border-orange-200 rounded-lg"
                        value={newCaregiver.email}
                        onChange={(e) =>
                            setNewCaregiver({ ...newCaregiver, email: e.target.value })
                        }
                        required
                    />
                    <input
                        type="tel"
                        placeholder="Phone"
                        className="p-2 border-2 border-orange-200 rounded-lg"
                        value={newCaregiver.phone}
                        onChange={(e) =>
                            setNewCaregiver({ ...newCaregiver, phone: e.target.value })
                        }
                        required
                    />
                    <input
                        type="text"
                        placeholder="Relationship"
                        className="p-2 border-2 border-orange-200 rounded-lg"
                        value={newCaregiver.relationship}
                        onChange={(e) =>
                            setNewCaregiver({ ...newCaregiver, relationship: e.target.value })
                        }
                        required
                    />
                    <label className="flex items-center space-x-2">
                        <input
                            type="checkbox"
                            className="form-checkbox h-5 w-5 text-orange-600"
                            checked={newCaregiver.emergency_contact}
                            onChange={(e) =>
                                setNewCaregiver({
                                    ...newCaregiver,
                                    emergency_contact: e.target.checked,
                                })
                            }
                        />
                        <span>Emergency Contact</span>
                    </label>
                </div>
                <button
                    type="submit"
                    className="mt-4 bg-orange-600 text-white px-6 py-3 rounded-lg hover:bg-orange-700"
                >
                    Add Caregiver
                </button>
            </form>

            {loading ? (
                <div className="text-center text-gray-600">Loading caregivers...</div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {caregivers.map((caregiver) => (
                        <div
                            key={caregiver.id}
                            className="bg-orange-100 p-4 rounded-lg shadow-md"
                        >
                            <h3 className="text-xl font-bold mb-2">{caregiver.name}</h3>
                            <p className="text-gray-600">📞 {caregiver.phone}</p>
                            <p className="text-gray-600">📧 {caregiver.email}</p>
                            <p className="text-blue-600 mt-2">
                                Relationship: {caregiver.relationship}
                            </p>
                            {caregiver.emergency_contact && (
                                <p className="text-red-600">🚨 Emergency Contact</p>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}