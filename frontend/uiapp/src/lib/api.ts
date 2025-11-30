import { browser } from '$app/environment';
import { auth } from './stores/auth';
import { get } from 'svelte/store';

const API_URL = 'http://localhost:8000/api';

interface RequestOptions extends RequestInit {
    token?: string;
}

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const url = `${API_URL}${endpoint}`;

    const headers = new Headers(options.headers);
    headers.set('Content-Type', 'application/json');

    const token = options.token || get(auth).token;
    if (token) {
        headers.set('Authorization', `Bearer ${token}`);
    }

    const config: RequestInit = {
        ...options,
        headers,
    };

    const response = await fetch(url, config);

    if (!response.ok) {
        if (response.status === 401) {
            auth.logout();
            if (browser) window.location.href = '/login';
        }
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `Error ${response.status}`);
    }

    if (response.status === 204) {
        return {} as T;
    }

    return response.json();
}

export const api = {
    get: <T>(endpoint: string, options?: RequestOptions) => request<T>(endpoint, { method: 'GET', ...options }),
    post: <T>(endpoint: string, body: any, options?: RequestOptions) => request<T>(endpoint, { method: 'POST', body: JSON.stringify(body), ...options }),
    put: <T>(endpoint: string, body: any, options?: RequestOptions) => request<T>(endpoint, { method: 'PUT', body: JSON.stringify(body), ...options }),
    delete: <T>(endpoint: string, options?: RequestOptions) => request<T>(endpoint, { method: 'DELETE', ...options }),
};
