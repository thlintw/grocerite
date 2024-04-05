import axios from 'axios';

export enum Endpoints {
    HouseholdsList = '/households',
    HouseholdsAdd = '/households/add',
    HouseholdsUpdate = '/households/{id}/update',
    HouseholdsDelete = '/households/{id}/delete',
}

export interface RequestOptions {
    method: 'GET' | 'POST' | 'PUT' | 'DELETE';
    headers?: Record<string, string>;
    data?: any; 
}
  
export class ApiService {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    private resolveUrl(url: Endpoints, params?: Record<string, string>): string {
        let resolvedUrl = url as string;
        if (params) {
            for (const key in params) {
                resolvedUrl = resolvedUrl.replace(`{${key}}`, encodeURIComponent(params[key]));
            }
        }
        return resolvedUrl;
    }

    async request<T>(endpoint: Endpoints, options: RequestOptions, params?: Record<string, string>): Promise<T> {
        const resolvedUrl = this.resolveUrl(endpoint, params);
        try {
            const response = await axios({
                method: options.method,
                url: `${this.baseUrl}${resolvedUrl}`,
                headers: options.headers,
                data: options.data,
            });
            return response.data as T;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                throw new Error(`Request failed: ${error.message}`);
            } else {
                throw new Error(`An unexpected error occurred: ${error}`);
            }
        }
    }

    async get<T>(endpoint: Endpoints, headers?: Record<string, string>, params?: Record<string, string>): Promise<T> {
        return this.request<T>(endpoint, { method: 'GET', headers }, params);
    }

    async post<T>(endpoint: Endpoints, data: any, headers?: Record<string, string>, params?: Record<string, string>): Promise<T> {
        return this.request<T>(endpoint, { method: 'POST', headers, data }, params);
    }

    async put<T>(endpoint: Endpoints, data: any, headers?: Record<string, string>, params?: Record<string, string>): Promise<T> {
        return this.request<T>(endpoint, { method: 'PUT', headers, data }, params);
    }

    async delete<T>(endpoint: Endpoints, headers?: Record<string, string>, params?: Record<string, string>): Promise<T> {
        return this.request<T>(endpoint, { method: 'DELETE', headers }, params);
    }
}
  