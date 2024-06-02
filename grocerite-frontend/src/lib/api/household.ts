import type { Container } from "$lib/models/container";
import type { Member } from "$lib/models/household";
import { ApiService, Endpoints, EndpointMethods, type RES } from "$lib/services/api";
import { userAuthHelper } from "./_helper";


export interface HouseholdCreateData {
    name: string;
    iconIdx: number;
    creater: Member
    containers: Container[];
}

export const createHousehold = async (): Promise<RES> => {
    const apiService = ApiService.getInstance();
    const userProfile = await userAuthHelper();
    return await apiService.get(
        Endpoints.CreateHousehold,
        {
            params: {
                userId: userProfile!.uid
            },
            needAuth: true
        }
    )
}