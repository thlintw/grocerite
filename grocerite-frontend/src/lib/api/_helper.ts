import { authStore } from "$lib/stores/authStore";
import type { User } from "firebase/auth";
import { get } from "svelte/store";

export const userAuthHelper = (): Promise<User> => {
    return new Promise((resolve, reject) => {
        if (!get(authStore).user) {
            const unsubscribe = authStore.subscribe(async ($authStore) => {
                const userProfile = $authStore.user;
                if (userProfile) {
                    unsubscribe();
                    resolve(userProfile);
                }
            });
        } else {
            const userProfile = get(authStore).user;
            resolve(userProfile!);
        }
    });
}