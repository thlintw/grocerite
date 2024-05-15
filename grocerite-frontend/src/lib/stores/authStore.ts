import type { User } from "firebase/auth";
import { writable } from 'svelte/store';
import type { UserProfile } from '$lib/models/userProfile';

interface AuthState {
    user: User | null; 
    userProfile: UserProfile | null;
    error: string | null;
    loading: boolean;
}

const initialState: AuthState = {
    user: null,
    userProfile: null,
    error: null,
    loading: false,
};

const createUserStore = () => {
    const { subscribe, set, update } = writable<AuthState>(initialState);

    return {
        subscribe,
        setUser: (user: User | null) => update((state) => ({ ...state, user })),
        setUserProfile: (userProfile: UserProfile | null) => update((state) => ({ ...state, userProfile })),
        setError: (error: string | null) => update((state) => ({ ...state, error })),
        setLoading: (loading: boolean) => update((state) => ({ ...state, loading })),
        reset: () => set(initialState),
    };
}

export const authStore = createUserStore();