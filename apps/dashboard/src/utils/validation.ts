/**
 * Form validation utilities
 * 
 * @created 2025-11-26
 */

export interface ValidationResult {
    valid: boolean;
    errors: string[];
}

/**
 * Validate email address
 */
export const validateEmail = (email: string): boolean => {
    const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
    return emailRegex.test(email);
};

/**
 * Validate password strength
 */
export const validatePassword = (password: string): ValidationResult => {
    const errors: string[] = [];

    if (password.length < 8) {
        errors.push('Password must be at least 8 characters long');
    }

    if (!/[A-Z]/.test(password)) {
        errors.push('Password must contain at least one uppercase letter');
    }

    if (!/[a-z]/.test(password)) {
        errors.push('Password must contain at least one lowercase letter');
    }

    if (!/[0-9]/.test(password)) {
        errors.push('Password must contain at least one number');
    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        errors.push('Password must contain at least one special character');
    }

    return {
        valid: errors.length === 0,
        errors,
    };
};

/**
 * Validate URL
 */
export const validateURL = (url: string): boolean => {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
};

/**
 * Validate IP address (IPv4)
 */
export const validateIPv4 = (ip: string): boolean => {
    const ipRegex = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (!ipRegex.test(ip)) return false;

    const parts = ip.split('.');
    return parts.every(part => {
        const num = parseInt(part, 10);
        return num >= 0 && num <= 255;
    });
};

/**
 * Validate username
 */
export const validateUsername = (username: string): ValidationResult => {
    const errors: string[] = [];

    if (username.length < 3) {
        errors.push('Username must be at least 3 characters long');
    }

    if (username.length > 20) {
        errors.push('Username must not exceed 20 characters');
    }

    if (!/^[a-zA-Z0-9_]+$/.test(username)) {
        errors.push('Username can only contain letters, numbers, and underscores');
    }

    return {
        valid: errors.length === 0,
        errors,
    };
};

/**
 * Validate required field
 */
export const validateRequired = (value: any, fieldName: string): ValidationResult => {
    const errors: string[] = [];

    if (!value || (typeof value === 'string' && value.trim() === '')) {
        errors.push(`${fieldName} is required`);
    }

    return {
        valid: errors.length === 0,
        errors,
    };
};

/**
 * Validate phone number
 */
export const validatePhone = (phone: string): boolean => {
    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
    return phoneRegex.test(phone) && phone.replace(/\D/g, '').length >= 10;
};
