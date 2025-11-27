/**
 * Mock/Fake Authentication Service for Development
 * Use this when backend is not available
 * 
 * @created 2025-11-26
 */

import { User } from '../services/authService';

// Fake admin user
export const FAKE_ADMIN: User = {
    id: 1,
    username: 'admin',
    email: 'admin@infinite.ai',
    full_name: 'Admin User',
    role: 'admin',
    is_active: true,
    created_at: new Date().toISOString(),
};

// Fake regular user
export const FAKE_USER: User = {
    id: 2,
    username: 'testuser',
    email: 'test@infinite.ai',
    full_name: 'Test User',
    role: 'user',
    is_active: true,
    created_at: new Date().toISOString(),
};

// Fake credentials database
const FAKE_USERS = [
    { email: 'admin@infinite.ai', password: 'admin123', user: FAKE_ADMIN },
    { email: 'test@infinite.ai', password: 'test123', user: FAKE_USER },
];

/**
 * Mock login function
 */
export const mockLogin = (email: string, password: string) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const user = FAKE_USERS.find(
                u => u.email === email && u.password === password
            );

            if (user) {
                const response = {
                    access_token: `fake_token_${Date.now()}`,
                    refresh_token: `fake_refresh_${Date.now()}`,
                    token_type: 'bearer',
                    user: user.user,
                };
                resolve(response);
            } else {
                reject(new Error('Invalid email or password'));
            }
        }, 500); // Simulate network delay
    });
};

/**
 * Mock register function
 */
export const mockRegister = (data: any) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            const newUser: User = {
                id: Math.floor(Math.random() * 1000),
                username: data.username,
                email: data.email,
                full_name: data.full_name || data.username,
                role: 'user',
                is_active: true,
                created_at: new Date().toISOString(),
            };

            const response = {
                access_token: `fake_token_${Date.now()}`,
                refresh_token: `fake_refresh_${Date.now()}`,
                token_type: 'bearer',
                user: newUser,
            };
            resolve(response);
        }, 500);
    });
};

/**
 * Mock stats for dashboard
 */
export const mockStats = {
    total_scans: 127,
    critical_threats: 8,
    resolved_issues: 342,
    active_agents: 5,
};

/**
 * Check if we're in development mode
 */
export const isDevelopmentMode = () => {
    return import.meta.env.DEV || import.meta.env.VITE_USE_MOCK_API === 'true';
};
