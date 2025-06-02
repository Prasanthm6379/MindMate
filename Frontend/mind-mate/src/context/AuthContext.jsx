// src/context/AuthContext.jsx
import { create } from 'zustand';
import { authAPI } from '../services/api';

export const useAuth = create((set) => ({
    user: null,
    token: null,

    login: async (email, password) => {
        try {
            const data = await authAPI.login(email, password);
            set({ user: { id: data.user_id }, token: data.token });
            localStorage.setItem('auth', JSON.stringify(data));
        } catch (error) {
            throw error;
        }
    },

    register: async (userData) => {
        try {
            const data = await authAPI.register(userData);
            set({ user: { id: data.user_id }, token: data.token });
            localStorage.setItem('auth', JSON.stringify(data));
        } catch (error) {
            throw error;
        }
    },

    logout: () => {
        set({ user: null, token: null });
        localStorage.removeItem('auth');
    },

    initialize: () => {
        const savedAuth = localStorage.getItem('auth');
        if (savedAuth) {
            const { user_id, token } = JSON.parse(savedAuth);
            set({ user: { id: user_id }, token });
        }
    }
}));