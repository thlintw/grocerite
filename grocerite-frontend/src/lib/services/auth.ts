import { auth } from '../firebaseConfig'; // Adjust the path as needed
import { authStore } from '../stores/authStore';
import { GoogleAuthProvider, signInWithPopup, OAuthProvider, signOut, onAuthStateChanged } from "firebase/auth";

export class AuthService {
    constructor() {
        onAuthStateChanged(auth, (user) => {
            if (user) {
                // User is signed in
                authStore.setUser(user);
                authStore.setError(null);
            } else {
                // User is signed out
                authStore.setUser(null);
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
            if (error instanceof Error) { // TypeScript type guard
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
            if (error instanceof Error) { // TypeScript type guard
                authStore.setError(error.message);
            } else {
                console.error("An unexpected error occurred", error);
            }
        } finally {
            authStore.setLoading(false);
        }
    }
}
  