import { writable } from 'svelte/store';
import { browser } from '$app/environment';

function createWebSocketStore() {
    const { subscribe, set, update } = writable<{
        socket: WebSocket | null;
        connected: boolean;
        message: any;
    }>({
        socket: null,
        connected: false,
        message: null
    });

    return {
        subscribe,
        connect: (slug: string) => {
            if (!browser) return;

            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//localhost:8000/ws/components/${slug}/`;
            const socket = new WebSocket(wsUrl);

            socket.onopen = () => {
                update(state => ({ ...state, connected: true }));
                console.log('WebSocket connected');
            };

            socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                update(state => ({ ...state, message: data }));
            };

            socket.onclose = () => {
                update(state => ({ ...state, connected: false, socket: null }));
                console.log('WebSocket disconnected');
            };

            update(state => ({ ...state, socket }));
        },
        sendMessage: (data: any) => {
            update(state => {
                if (state.socket && state.socket.readyState === WebSocket.OPEN) {
                    state.socket.send(JSON.stringify(data));
                }
                return state;
            });
        },
        disconnect: () => {
            update(state => {
                if (state.socket) {
                    state.socket.close();
                }
                return { socket: null, connected: false, message: null };
            });
        }
    };
}

export const ws = createWebSocketStore();
