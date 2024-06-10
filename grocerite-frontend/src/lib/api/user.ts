import { ApiService, Endpoints, EndpointMethods, type RES } from "$lib/services/api";
import type { User } from "firebase/auth";
import { userAuthHelper } from "./_helper";
import { authStore } from "$lib/stores/authStore";
import { UserProfile } from "$lib/models/userProfile";


export interface UserProfileCreate {
    email: string;
    username: string;
    fb_uid: string;
}

export const reloadUserProfile = async (): Promise<boolean> => {
    try {
        const user = await userAuthHelper();
        const res: RES = await getUserProfileFromFbUid(user);
        if (res.status === 'S') {
            authStore.setUserProfile(UserProfile.fromJson(res.data[0]));
            return true;
        } else {
            console.error('Failed to reload user profile');
            return false;
        }
    } catch (_) {
        console.error('Failed to reload user profile');
        return false;
    }    
}

export const getUserProfileFromFbUid = async (user: User): Promise<RES> => {
    const apiService = ApiService.getInstance();
    return await apiService.get(
        Endpoints.GetUserProfileFromFbUid,
        {
            params: {
                fbUid: user.uid
            }
        }
    );

}

export const createUserProfile = async (data: UserProfileCreate): Promise<RES> => {
    const apiService = ApiService.getInstance();
    return await apiService.post(
        Endpoints.CreateUserProfile,
        {
            data: data
        }
    );
}