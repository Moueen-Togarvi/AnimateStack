import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface User {
    id: number;
    email: string;
    username: string;
    is_creator: boolean;
    avatar?: string;
}

interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
}

const initialState: AuthState = {
    user: null,
    token: null,
    isAuthenticated: false,
};

function createAuthStore() {
    const { subscribe, set, update } = writable<AuthState>(initialState);

    return {
        subscribe,
        login: (user: User, token: string) => {
            if (browser) {
                localStorage.setItem('token', token);
                localStorage.setItem('user', JSON.stringify(user));
            }
            set({ user, token, isAuthenticated: true });
        },
        logout: () => {
            if (browser) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }
            set(initialState);
        },
        initialize: () => {
            if (browser) {
                const token = localStorage.getItem('token');
                const userStr = localStorage.getItem('user');
                if (token && userStr) {
                    set({ user: JSON.parse(userStr), token, isAuthenticated: true });
                }
            }
        }
    };
}

export const auth = createAuthStore();
