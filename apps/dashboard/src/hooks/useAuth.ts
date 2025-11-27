/**
 * Authentication Hook
 * 
 * @created 2025-11-26
 */

import { useState, useEffect, useCallback } from 'react';
import { authService, User, LoginCredentials, RegisterData } from '../services';

export const useAuth = () => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Initialize auth state
    useEffect(() => {
        const initAuth = async () => {
            try {
                if (authService.isAuthenticated()) {
                    const currentUser = authService.getCurrentUser();
                    setUser(currentUser);
                }
            } catch (err) {
                console.error('Auth initialization error:', err);
            } finally {
                setLoading(false);
            }
        };

        initAuth();
    }, []);

    // Login
    const login = useCallback(async (credentials: LoginCredentials) => {
        setLoading(true);
        setError(null);

        try {
            const response = await authService.login(credentials);
            setUser(response.user);
            return response;
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || 'Login failed';
            setError(errorMsg);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    // Register
    const register = useCallback(async (data: RegisterData) => {
        setLoading(true);
        setError(null);

        try {
            const response = await authService.register(data);
            setUser(response.user);
            return response;
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || 'Registration failed';
            setError(errorMsg);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    // Logout
    const logout = useCallback(async () => {
        setLoading(true);

        try {
            await authService.logout();
            setUser(null);
        } catch (err) {
            console.error('Logout error:', err);
        } finally {
            setLoading(false);
        }
    }, []);

    // Update profile
    const updateProfile = useCallback(async (data: Partial<User>) => {
        setLoading(true);
        setError(null);

        try {
            const updatedUser = await authService.updateProfile(data);
            setUser(updatedUser);
            localStorage.setItem('user', JSON.stringify(updatedUser));
            return updatedUser;
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || 'Profile update failed';
            setError(errorMsg);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    return {
        user,
        loading,
        error,
        isAuthenticated: !!user,
        login,
        register,
        logout,
        updateProfile,
    };
};

export default useAuth;
