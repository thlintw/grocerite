import type { User } from "firebase/auth";
import { writable } from 'svelte/store';

interface AuthState {
    user: User | null; 
    groceriteProfile: any;
    error: string | null;
    loading: boolean;
}

const initialState: AuthState = {
    user: null,
    groceriteProfile: null,
    error: null,
    loading: false,
};

function createUserStore() {
    const { subscribe, set, update } = writable<AuthState>(initialState);

    return {
        subscribe,
        setUser: (user: User | null) => update((state) => ({ ...state, user })),
        setError: (error: string | null) => update((state) => ({ ...state, error })),
        setLoading: (loading: boolean) => update((state) => ({ ...state, loading })),
        reset: () => set(initialState),
    };
}

export const authStore = createUserStore();