import { onAuthStateChanged, type User } from "firebase/auth";
import { writable } from 'svelte/store';
import type { UserProfile } from '$lib/models/userProfile';
import { auth } from '$lib/firebaseConfig'

interface AuthState {
    user: User | null; 
    userProfile: UserProfile | null;
    error: string | null;
    loading: boolean;
    authStateChecked: boolean;
}

const initialState: AuthState = {
    user: null,
    userProfile: null,
    error: null,
    loading: false,
    authStateChecked: false
};

const createUserStore = () => {
    const { subscribe, set, update } = writable<AuthState>(initialState);

    return {
        subscribe,
        setUser: (user: User | null) => update((state) => ({ ...state, user })),
        setUserProfile: (userProfile: UserProfile | null) => update((state) => ({ ...state, userProfile })),
        setError: (error: string | null) => update((state) => ({ ...state, error })),
        setLoading: (loading: boolean) => update((state) => ({ ...state, loading })),
        setAuthStateChecked: (authStateChecked: boolean) => update((state) => ({ ...state, authStateChecked })),
        reset: () => set(initialState),
    };
}

export const authStore = createUserStore();