import type { Container } from "$lib/models/container";
import type { Member } from "$lib/models/household";
import { ApiService, Endpoints, EndpointMethods, type RES } from "$lib/services/api";
import { userAuthHelper } from "./_helper";
import { authStore } from "$lib/stores/authStore";
import { get } from "svelte/store";


export interface HouseholdCreateData {
    name: string;
    iconIdx: number;
    creator: {
        name: string;
        pfpIdx: number;
        pfpBgColor: string;
        pfpPresenting: string;
    }
    containers: {
        type: string;
        name: string;
    }[];
}

export const apiCreateHousehold = async (postData: HouseholdCreateData): Promise<RES> => {
    const apiService = ApiService.getInstance();
    await userAuthHelper();
    return await apiService.post(
        Endpoints.CreateHousehold,
        {
            params: {
                userId: get(authStore).userProfile!.userId,
            },
            needAuth: true,
            data: postData
        }
    )
}

export const apiGetHousehold = async (householdId: string): Promise<RES> => {
    const apiService = ApiService.getInstance();
    await userAuthHelper();
    return await apiService.get(
        Endpoints.GetHousehold,
        {
            params: {
                householdId: householdId
            },
            needAuth: true
        }
    )
}

export const apiListHouseholds = async (): Promise<RES> => {
    const apiService = ApiService.getInstance();
    await userAuthHelper();
    return await apiService.get(
        Endpoints.ListHouseholds,
        {
            params: {
                userId: get(authStore).userProfile!.userId,
            },
            needAuth: true
        }
    )
}

export const apiSetActiveHousehold = async (householdId: string): Promise<RES> => {
    const apiService = ApiService.getInstance();
    await userAuthHelper();
    return await apiService.put(
        Endpoints.SetActiveHousehold,
        {
            params: {
                householdId: householdId,
                userId: get(authStore).userProfile!.userId,
            },
            needAuth: true
        }
    )
}