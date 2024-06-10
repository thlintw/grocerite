import axios from 'axios';
import { authStore } from '$lib/stores/authStore';
import { get } from 'svelte/store';

export enum Endpoints {
    // misc
    WakeUp = '/wake_up',
    // home
    HomeDashboard = '/dashboard/$userId',
    // household
    ListHouseholds = '/household/$userId',
    GetHousehold = '/household/get/$householdId',
    SetActiveHousehold = '/household/set_active/$userId/$householdId',
    CreateHousehold = '/household/create/$userId',
    UpdateHousehold = '/household/update/$householdId',
    UpdateHouseholdName = '/household/update_name/$householdId',
    UpdateHouseholdIcon = '/household/update_icon/$householdId',
    DeleteHousehold = '/household/delete/$householdId',
    AddHouseholdMember = '/household/add_member/$householdId',
    DeleteHouseholdMember = '/household/delete_member/$householdId/$memberIdx',
    UpdateHouseholdContainer = '/household/update_container/$householdId/$containerIdx',
    ManageHouseholdContainerItem = '/household/manage_item/$householdId/$containerIdx/$containerItemIdx',
    DeleteContainer = '/household/delete_container/$householdId/$containerIdx',
    BulkAddItemToList = '/household/bulk_add_item_to_list/$householdId/$containerIdx',
    CreateContainer = '/household/create_container/$householdId',
    // grocery list
    ListGroceryLists = '/grocery_list/$householdId',
    GetGroceryList = '/grocery_list/get/$groceryListId',
    CreateGroceryList = '/grocery_list/create/$householdId',
    UpdateGroceryList = '/grocery_list/update/$groceryListId',
    DeleteGroceryList = '/grocery_list/delete/$groceryListId',
    TickGroceryListItem = '/grocery_list/tick_item/$groceryListId/$groceryListItemIdx',
    TickAllGroceryListItems = '/grocery_list/tick_all_items/$groceryListId',
    UntickGroceryListItem = '/grocery_list/untick_item/$groceryListId/$groceryListItemIdx',
    EditGroceryListItem = '/grocery_list/edit_item/$groceryListId/$groceryListItemIdx',
    DeleteGroceryListItem = '/grocery_list/delete_item/$groceryListId/$groceryListItemIdx',
    GetAvailableItems = '/grocery_list/available_items/$householdId',
    // user
    GetUserProfileFromFbUid = '/profile_from_fb/$fbUid',
    GetUserProfile = '/profile/get/$userId',
    CreateUserProfile = '/profile/create',
    GetUserPreferences = '/profile/preferences/$userId',
    SetUserPreferences = '/profile/preferences/set/$userId',
}

export const EndpointMethods = {
    [Endpoints.WakeUp]: 'GET',
    [Endpoints.HomeDashboard]: 'GET',
    [Endpoints.ListHouseholds]: 'GET',
    [Endpoints.GetHousehold]: 'GET',
    [Endpoints.SetActiveHousehold]: 'PUT',
    [Endpoints.CreateHousehold]: 'POST',
    [Endpoints.UpdateHousehold]: 'PUT',
    [Endpoints.UpdateHouseholdName]: 'PUT',
    [Endpoints.UpdateHouseholdIcon]: 'PUT',
    [Endpoints.DeleteHousehold]: 'DELETE',
    [Endpoints.AddHouseholdMember]: 'POST',
    [Endpoints.DeleteHouseholdMember]: 'DELETE',
    [Endpoints.UpdateHouseholdContainer]: 'PUT',
    [Endpoints.ManageHouseholdContainerItem]: 'PUT',
    [Endpoints.DeleteContainer]: 'DELETE',
    [Endpoints.BulkAddItemToList]: 'POST',
    [Endpoints.CreateContainer]: 'POST',
    [Endpoints.ListGroceryLists]: 'GET',
    [Endpoints.GetGroceryList]: 'GET',
    [Endpoints.CreateGroceryList]: 'POST',
    [Endpoints.UpdateGroceryList]: 'PUT',
    [Endpoints.DeleteGroceryList]: 'DELETE',
    [Endpoints.TickGroceryListItem]: 'PUT',
    [Endpoints.TickAllGroceryListItems]: 'PUT',
    [Endpoints.UntickGroceryListItem]: 'PUT',
    [Endpoints.EditGroceryListItem]: 'PUT',
    [Endpoints.DeleteGroceryListItem]: 'DELETE',
    [Endpoints.GetAvailableItems]: 'GET',
    [Endpoints.GetUserProfile]: 'GET',
    [Endpoints.CreateUserProfile]: 'POST',
    [Endpoints.GetUserPreferences]: 'GET',
    [Endpoints.SetUserPreferences]: 'PUT',
}


export interface RequestOptions {
    method: 'GET' | 'POST' | 'PUT' | 'DELETE';
    needAuth?: boolean;
    headers?: Record<string, string>;
    data?: any; 
}

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL as string;

export interface RES {
    status: 'S' | 'F';
    message: string;
    data: any[];
}

  
export class ApiService {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    static getInstance(): ApiService {
        return new ApiService(apiBaseUrl);
    }

    private resolveUrl(url: Endpoints, params?: Record<string, string | number>): string {
        let resolvedUrl = url as string;
        const placeholderRegex = /\$[a-zA-Z0-9_]+/g;
        const matches = resolvedUrl.match(placeholderRegex);

        if (matches && params) {
            matches.forEach(match => {
                const paramName = match.slice(1);
                const paramValue = params[paramName];
                if (paramValue === undefined || paramValue === null) {
                    throw new Error(`Parameter "${paramName}" is required`);
                }
                resolvedUrl = resolvedUrl.replace(match, encodeURIComponent(String(paramValue)));
            });
        } else if (matches) {
            throw new Error('Parameters are required but not provided');
        } else if (params && params.length as number > 0) {
            throw new Error('No parameters are required but provided');
        }

        return resolvedUrl;
    }

    private makeAuthHeader(): Record<string, string> {
        const user = get(authStore).user;
        if (!user) {
            throw new Error('User is not authenticated');
        }
        return {
            Authorization: `Bearer ${user.getIdToken()}`,
        };
    }
        

    async request<T>(
        endpoint: Endpoints,
        {
            options,
            params,
            data
        }: 
        {
            options: RequestOptions,
            params?: Record<string, string | number>,
            data?: Record<string, any>
        }
    ): Promise<T> {
        const resolvedUrl = this.resolveUrl(endpoint, params);
        if (options && options.needAuth) {
            options.headers = {
                ...options.headers,
                ...this.makeAuthHeader(),
            };
        }
        try {
            const response = await axios({
                method: options!.method,
                url: `${this.baseUrl}${resolvedUrl}`,
                headers: options.headers,
                data: options.data,
            });
            console.log(response);
            return response.data as T;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.log(error.response);
                throw new Error(`Request failed: ${error.message}`);
            } else {
                throw new Error(`An unexpected error occurred: ${error}`);
            }
        }
    }

    async get<T>(
        endpoint: Endpoints,
        {
            headers = {},
            params = {},
            needAuth = false
        }: 
        {
            headers?: Record<string, string>,
            params?: Record<string, string | number>,
            needAuth?: boolean
        } = {}
    ): Promise<T> {
        return this.request<T>(endpoint, { options: { method: 'GET', headers, needAuth }, params });
    }

    async post<T>(
        endpoint: Endpoints,
        {
            headers = {},
            params = {},
            data = {},
            needAuth = false
        }:
        {
            headers?: Record<string, string>,
            params?: Record<string, string | number>,
            data?: Record<string, any>,
            needAuth?: boolean
        } = {}
    ): Promise<T> {
        return this.request<T>(endpoint, { options: { method: 'POST', headers, needAuth, data }, params });
    }

    async put<T>(
        endpoint: Endpoints,
        {
            headers = {},
            params = {},
            needAuth = false,
            data = {}
        }:
        {
            headers?: Record<string, string>,
            params?: Record<string, string | number>,
            needAuth?: boolean,
            data?: Record<string, any>
        } = {}
    ): Promise<T> {
        return this.request<T>(endpoint, { options: { method: 'PUT', headers, needAuth, data }, params });
    }

    async delete<T>(
        endpoint: Endpoints,
        {
            headers = {},
            params = {},
            needAuth = false,
            data = {}
        }:
        {
            headers?: Record<string, string>,
            params?: Record<string, string | number>,
            needAuth?: boolean,
            data?: Record<string, any>
        } = {}
    ): Promise<T> {
        return this.request<T>(endpoint, { options: { method: 'DELETE', headers, needAuth, data }, params });
    }
}
  