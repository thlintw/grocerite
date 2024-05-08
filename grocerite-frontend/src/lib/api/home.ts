import { ApiService, type RES, Endpoints, EndpointMethods } from "$lib/services/api";
import { authStore } from "$lib/stores/authStore";
import { get } from "svelte/store";


export const wakeUp = async (): Promise<RES> => {
    const apiService = ApiService.getInstance();
    return apiService.get(Endpoints.WakeUp);
}

export const dashboard = async (): Promise<RES> => {
    const apiService = ApiService.getInstance();
    const userProfile = get(authStore).userProfile;
    if (!userProfile) {
        throw new Error('user not authenticated');
    }
    return apiService.get(Endpoints.HomeDashboard);
}