/**
 * API Client Configuration
 * 
 * @created 2025-11-26
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
const API_TIMEOUT = 30000; // 30 seconds

// Create axios instance
const apiClient: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: API_TIMEOUT,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
apiClient.interceptors.request.use(
    (config) => {
        // Add auth token if available
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('[API] Request error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor
apiClient.interceptors.response.use(
    (response: AxiosResponse) => {
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        // Handle 401 Unauthorized
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Try to refresh token
                const refreshToken = localStorage.getItem('refresh_token');
                if (refreshToken) {
                    const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
                        refresh_token: refreshToken,
                    });

                    const { access_token } = response.data;
                    localStorage.setItem('access_token', access_token);

                    // Retry original request
                    originalRequest.headers.Authorization = `Bearer ${access_token}`;
                    return apiClient(originalRequest);
                }
            } catch (refreshError) {
                // Refresh failed, logout user
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        // Handle other errors
        console.error('[API] Response error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
);

// API helper functions
export const api = {
    get: <T = any>(url: string, config?: AxiosRequestConfig) =>
        apiClient.get<T>(url, config).then(res => res.data),

    post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig) =>
        apiClient.post<T>(url, data, config).then(res => res.data),

    put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig) =>
        apiClient.put<T>(url, data, config).then(res => res.data),

    patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig) =>
        apiClient.patch<T>(url, data, config).then(res => res.data),

    delete: <T = any>(url: string, config?: AxiosRequestConfig) =>
        apiClient.delete<T>(url, config).then(res => res.data),
};

export default apiClient;
