import { ApiService, Endpoints, EndpointMethods, type RES } from "$lib/services/api";
import { userAuthHelper } from "./_helper";



export const listGroceryLists = async (householdId: string): Promise<RES> => {
    const apiService = ApiService.getInstance();
    await userAuthHelper();
    return await apiService.get(
        Endpoints.ListGroceryLists,
        {
            params: {
                householdId: householdId
            },
            needAuth: true
        }
    )
}