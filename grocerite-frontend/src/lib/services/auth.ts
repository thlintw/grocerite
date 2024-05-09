import { auth } from '../firebaseConfig'; // Adjust the path as needed
import { authStore } from '../stores/authStore';
import { GoogleAuthProvider, signInWithPopup, OAuthProvider, signOut, onAuthStateChanged } from "firebase/auth";

export class AuthService {
    static instance: AuthService | null = null;
    authenticated: boolean = false;

    private constructor() {
        this.initializeAuthListener();
    }

    static getInstance(): AuthService {
        if (!AuthService.instance) {
            AuthService.instance = new AuthService();
        }
        return AuthService.instance;
    }

    private initializeAuthListener() {
        
        onAuthStateChanged(auth, (user) => {
            if (user) {
                authStore.setUser(user);
                authStore.setError(null);
                this.authenticated = true;
            } else {
                authStore.setUser(null);
                authStore.setError(null);
                this.authenticated = false;
            }
            authStore.setLoading(false);
        });
    }
  
    async signInWithGoogle(): Promise<void> {
        const provider = new GoogleAuthProvider();
        try {
            authStore.setLoading(true);
            const result = await signInWithPopup(auth, provider);
            authStore.setUser(result.user);
            authStore.setError(null);
        } catch (error) {
            if (error instanceof Error) { 
                authStore.setError(error.message);
            } else {
                console.error("An unexpected error occurred", error);
            }
        } finally {
            authStore.setLoading(false);
        }
    }
  
    async signOutUser(): Promise<void> {
        try {
            authStore.setLoading(true);
            await signOut(auth);
            authStore.setUser(null);
            authStore.setError(null);
        } catch (error) {
            if (error instanceof Error) {
                authStore.setError(error.message);
            } else {
                console.error("An unexpected error occurred", error);
            }
        } finally {
            authStore.setLoading(false);
        }
    }
}
  