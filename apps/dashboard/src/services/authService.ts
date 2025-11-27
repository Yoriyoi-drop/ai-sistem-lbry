/**
 * Authentication Service
 * 
 * @created 2025-11-26
 */

import { api } from './api';
import { mockLogin, mockRegister, isDevelopmentMode } from './mockAuth';

export interface LoginCredentials {
    email: string;
    password: string;
}

export interface RegisterData {
    username: string;
    email: string;
    password: string;
    full_name?: string;
}

export interface AuthResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
    user: User;
}

export interface User {
    id: number;
    username: string;
    email: string;
    full_name?: string;
    role: string;
    is_active: boolean;
    created_at: string;
}

class AuthService {
    /**
     * Login user
     */
    async login(credentials: LoginCredentials): Promise<AuthResponse> {
        try {
            const response = await api.post<AuthResponse>('/auth/login', credentials);

            // Store tokens
            localStorage.setItem('access_token', response.access_token);
            localStorage.setItem('refresh_token', response.refresh_token);
            localStorage.setItem('user', JSON.stringify(response.user));

            return response;
        } catch (error) {
            // Fallback to mock auth in development
            if (isDevelopmentMode()) {
                console.warn('🎭 Using mock authentication (backend not available)');
                const response = await mockLogin(credentials.email, credentials.password) as AuthResponse;

                // Store tokens
                localStorage.setItem('access_token', response.access_token);
                localStorage.setItem('refresh_token', response.refresh_token);
                localStorage.setItem('user', JSON.stringify(response.user));

                return response;
            }
            throw error;
        }
    }

    /**
     * Register new user
     */
    async register(data: RegisterData): Promise<AuthResponse> {
        try {
            const response = await api.post<AuthResponse>('/auth/register', data);

            // Store tokens
            localStorage.setItem('access_token', response.access_token);
            localStorage.setItem('refresh_token', response.refresh_token);
            localStorage.setItem('user', JSON.stringify(response.user));

            return response;
        } catch (error) {
            // Fallback to mock auth in development
            if (isDevelopmentMode()) {
                console.warn('🎭 Using mock registration (backend not available)');
                const response = await mockRegister(data) as AuthResponse;

                // Store tokens
                localStorage.setItem('access_token', response.access_token);
                localStorage.setItem('refresh_token', response.refresh_token);
                localStorage.setItem('user', JSON.stringify(response.user));

                return response;
            }
            throw error;
        }
    }

    /**
     * Logout user
     */
    async logout(): Promise<void> {
        try {
            await api.post('/auth/logout');
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            // Clear local storage
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
        }
    }

    /**
     * Get current user
     */
    getCurrentUser(): User | null {
        const userStr = localStorage.getItem('user');
        const token = localStorage.getItem('access_token');
        if (!userStr || !token) return null;

        try {
            return JSON.parse(userStr);
        } catch {
            return null;
        }
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated(): boolean {
        return !!localStorage.getItem('access_token');
    }

    /**
     * Get user profile
     */
    async getProfile(): Promise<User> {
        return api.get<User>('/auth/me');
    }

    /**
     * Update user profile
     */
    async updateProfile(data: Partial<User>): Promise<User> {
        return api.put<User>('/auth/me', data);
    }

    /**
     * Change password
     */
    async changePassword(oldPassword: string, newPassword: string): Promise<void> {
        await api.post('/auth/change-password', {
            old_password: oldPassword,
            new_password: newPassword,
        });
    }

    /**
     * Request password reset
     */
    async requestPasswordReset(email: string): Promise<void> {
        await api.post('/auth/forgot-password', { email });
    }

    /**
     * Reset password with token
     */
    async resetPassword(token: string, newPassword: string): Promise<void> {
        await api.post('/auth/reset-password', {
            token,
            new_password: newPassword,
        });
    }
}

export const authService = new AuthService();
export default authService;
