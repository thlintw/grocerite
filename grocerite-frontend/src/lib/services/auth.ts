import { auth } from '../firebaseConfig'; // Adjust the path as needed
import { authStore } from '../stores/authStore';
import { GoogleAuthProvider, signInWithPopup, OAuthProvider, signOut, onAuthStateChanged, browserSessionPersistence, setPersistence, browserLocalPersistence } from "firebase/auth";
import { getUserProfileFromFbUid, createUserProfile } from '$lib/api/user';
import type { RES } from './api';
import { UserProfile } from '$lib/models/userProfile';
import { toast } from '@zerodevx/svelte-toast';

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
        
        onAuthStateChanged(auth, async (user) => {
            if (user) {
                console.log('User is signed in');
                console.log(user);
                authStore.setUser(user);
                authStore.setError(null);
                const userProfileRes: RES = await getUserProfileFromFbUid(user);
                try {
                    const userProfile = UserProfile.fromJson(userProfileRes.data[0]);
                    authStore.setUserProfile(userProfile);
                } catch (error) {
                    toast.push('Failed to fetch user profile')
                    await this.signOutUser();
                }
                this.authenticated = true;
            } else {
                authStore.setUser(null);
                authStore.setError(null);
                this.authenticated = false;
            }
            authStore.setLoading(false);
            authStore.setAuthStateChecked(true);
        });
    }
  
    async signInWithGoogle(): Promise<void> {
        const provider = new GoogleAuthProvider();
        try {
            authStore.setLoading(true);
            const result = await signInWithPopup(auth, provider);
            const userProfileRes: RES = await getUserProfileFromFbUid(result.user);
            let userProfile: UserProfile;
            if (userProfileRes.data.length === 0) {
                const apiCreateUserprofileRes: RES = await createUserProfile({
                    email: result.user.email!,
                    username: result.user.email!,
                    fb_uid: result.user.uid
                });
                userProfile = UserProfile.fromJson(apiCreateUserprofileRes.data[0]);
            } else {
                userProfile = UserProfile.fromJson(userProfileRes.data[0]);
            }
            authStore.setUser(result.user);
            authStore.setUserProfile(userProfile!);
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
            authStore.setUserProfile(null);
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
  