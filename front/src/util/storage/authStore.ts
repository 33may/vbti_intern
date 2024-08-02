import { create } from 'zustand';
import {decodeToken, isTokenExpired} from "../jwt.ts";
import DecodedToken from '../jwt.ts';

interface AuthState {
    token: string | null;
    isAuthenticated: boolean;
    user: DecodedToken | null;
    setToken: (token: string | null) => void;
    clearToken: () => void;
}

const useAuthStore = create<AuthState>((set) => ({
    token: localStorage.getItem('token'),

    isAuthenticated: !!localStorage.getItem('token') && !isTokenExpired(localStorage.getItem('token')!),

    user: localStorage.getItem('token') ? decodeToken(localStorage.getItem('token')!) : null,

    setToken: (token) => {
        if (token) {
            localStorage.setItem('token', token);
            set({ token, isAuthenticated: true, user: decodeToken(token) });
        } else {
            localStorage.removeItem('token');
            set({ token: null, isAuthenticated: false, user: null });
        }
    },

    clearToken: () => {
        localStorage.removeItem('token');
        set({ token: null, isAuthenticated: false, user: null });
    },
}));

export default useAuthStore;
