// src/services/api.js
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000',
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
    // Skip adding the token for login and register endpoints
    if (config.url === '/user/login' || config.url === '/user/') {
        return config;
    }

    // Get the token from sessionStorage
    const token = sessionStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const authAPI = {
    login: async (email, password) => {
        try {
            const response = await api.post('/user/login', { email, password });
            console.log(response.data.data.message.user_id);
            
            // Store the token in sessionStorage
            sessionStorage.setItem('token', response.data.data.token.token);
            sessionStorage.setItem('user_id',response.data.data.message.user_id);
            return response.data; // Should return { token, user_id }
        } catch (error) {
            console.log(error);
            throw error.response.data;
        }
    },
    register: async (userData) => {
        try {
            const response = await api.post('/user/', userData);
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    }
};

export const memoryNoteAPI = {
    create: async (userId, noteData, isImage = false) => {
        const formData = new FormData();

        if (isImage) {
            formData.append('note_type', 'img');
            formData.append('content', noteData.file);
        } else {
            formData.append('note_type', 'note');
            formData.append('content', noteData.content);
        }

        formData.append('title', noteData.title);

        try {
            console.log(userId);
            
            const response = await api.post(
                `/user/memoryNote/${userId}`,
                formData,
                { headers: { 'Content-Type': 'multipart/form-data' } }
            );
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },

    getAll: async (userId) => {
        try {
            const response = await api.get(`/user/memoryNote/${userId}`);
            console.log(response.data);
            
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },

    update: async (userId, noteId, updateData) => {
        try {
            const response = await api.put(
                `/user/memoryNote/${userId}`,
                { ...updateData, id: noteId }
            );
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },

    delete: async (userId, noteId) => {
        try {
            const response = await api.delete(
                `/user/memoryNote/${userId}/${noteId}`
            );
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    }
};

export const emergencyAPI = {
    createAlert: async (alertData) => {
        try {
            const response = await api.post(`/user/emergencyalert/${alertData.user_id}`, alertData);
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },

    getAlerts: async (userId) => {
        try {
            const response = await api.get(`/user/emergencyalert/${userId}`);
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    }
};

export const caregiverAPI = {
    addCaregiver: async (caregiverData) => {
        try {
            const response = await api.post(`/user/caregiver/${caregiverData.user_id}`, caregiverData);
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },

    getCaregivers: async (userId) => {
        try {
            const response = await api.get(`/user/caregiver/${userId}`);
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    }
};

export const reminderAPI = {
    createReminder: async (reminderData) => {
        try {
            console.log(reminderData);
            
            const response = await api.post(`/user/remainder/${reminderData.user_id}`, reminderData);
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },

    getReminders: async (userId) => {
        try {
            const response = await api.get(`/user/remainder/${userId}`);
            console.log(response.data,"Reminders");
            
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    }
};

export const activityAPI = {
    // Create a new activity
    createActivity: async (activityData) => {
        try {
            console.log(activityData);
            
            const response = await api.post(`/user/activitylog/${activityData.user_id}`, activityData);
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },

    // Get all activities for a user
    getActivities: async (user_id) => {
        try {
            const response = await api.get(`/user/activitylog/${user_id}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    },

    // Get a single activity by ID
    getActivityById: async (activityId) => {
        try {
            const response = await api.get(`/user/activitylog/${activityId}`);
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },

    // Update an existing activity
    updateActivity: async (activityId, updateData) => {
        try {
            const response = await api.put(`/user/activitylog`, {
                id: activityId,
                ...updateData,
            });
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },

    // Delete an activity
    deleteActivity: async (activityId) => {
        try {
            const response = await api.delete(`/user/activitylog`, {
                data: { id: activityId },
            });
            return response.data;
        } catch (error) {
            throw error.response.data;
        }
    },
};