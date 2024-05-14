import { ApiService, type RES, Endpoints } from "$lib/services/api";
import { userAuthHelper } from "./_helper";

export const wakeUp = async (): Promise<RES> => {
    const apiService = ApiService.getInstance();
    return apiService.get(Endpoints.WakeUp);
}

export const dashboard = async (): Promise<RES> => {
    const apiService = ApiService.getInstance();
    const userProfile = await userAuthHelper();
    return await apiService.get(
        Endpoints.HomeDashboard, 
        { 
            params: {
                userId: userProfile!.uid
            },
            needAuth: true
        }
    )
}