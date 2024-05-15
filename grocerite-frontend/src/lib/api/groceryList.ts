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

export const getGroceryList = async (groceryListId: string): Promise<RES> => {
    const apiService = ApiService.getInstance();
    await userAuthHelper();
    return await apiService.get(
        Endpoints.GetGroceryList,
        {
            params: {
                groceryListId: groceryListId
            },
            needAuth: true
        }
    )
}


export interface GroceryListCreateData {
    name: string;
    iconIdx: number;
    description: string;
    assigneeMemberIdx: number;
    deadline: string;
    items: {
        itemIdx: number;
        name: string;
        category: string;
        quantity: number;
        containerIdx: number;
    }[]
}

export const createGroceryList = async (householdId: string, data: GroceryListCreateData): Promise<RES> => {
    const apiService = ApiService.getInstance();
    await userAuthHelper();
    return await apiService.post(
        Endpoints.CreateGroceryList,
        {
            params: {
                householdId: householdId,
            },
            data: data,
        }
    )
}