import { ApiService, Endpoints, EndpointMethods, type RES } from "$lib/services/api";
import type { User } from "firebase/auth";
import { userAuthHelper } from "./_helper";


export interface UserProfileCreate {
    email: string;
    username: string;
    fb_uid: string;
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