/**
 * Application constants
 * 
 * @created 2025-11-26
 */

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
export const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

// Application Routes
export const ROUTES = {
    HOME: '/',
    LOGIN: '/login',
    REGISTER: '/register',
    FORGOT_PASSWORD: '/forgot-password',
    DASHBOARD: '/dashboard',
    AGENTS: '/agents',
    SECURITY: '/security',
    SCANS: '/scans',
    SETTINGS: '/settings',
    PROFILE: '/profile',
} as const;

// Agent Types
export const AGENT_TYPES = {
    SCANNER: 'security_scanner',
    DETECTOR: 'threat_detector',
    ANALYZER: 'vulnerability_analyzer',
    LABYRINTH: 'labyrinth_defense',
} as const;

// Agent Status
export const AGENT_STATUS = {
    ACTIVE: 'active',
    INACTIVE: 'inactive',
    ERROR: 'error',
    MAINTENANCE: 'maintenance',
} as const;

// Scan Types
export const SCAN_TYPES = {
    VULNERABILITY: 'vulnerability',
    MALWARE: 'malware',
    NETWORK: 'network',
    COMPLIANCE: 'compliance',
    PENETRATION: 'penetration',
} as const;

// Scan Status
export const SCAN_STATUS = {
    PENDING: 'pending',
    RUNNING: 'running',
    COMPLETED: 'completed',
    FAILED: 'failed',
    CANCELLED: 'cancelled',
} as const;

// Threat Levels
export const THREAT_LEVELS = {
    CRITICAL: 'critical',
    HIGH: 'high',
    MEDIUM: 'medium',
    LOW: 'low',
    INFO: 'info',
} as const;

// Severity Colors
export const SEVERITY_COLORS = {
    critical: '#dc2626',
    high: '#ea580c',
    medium: '#f59e0b',
    low: '#10b981',
    info: '#3b82f6',
} as const;

// Status Colors
export const STATUS_COLORS = {
    active: '#10b981',
    inactive: '#6b7280',
    error: '#dc2626',
    maintenance: '#f59e0b',
    pending: '#f59e0b',
    running: '#3b82f6',
    completed: '#10b981',
    failed: '#dc2626',
    cancelled: '#6b7280',
} as const;

// Pagination
export const DEFAULT_PAGE_SIZE = 20;
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];

// Local Storage Keys
export const STORAGE_KEYS = {
    ACCESS_TOKEN: 'access_token',
    REFRESH_TOKEN: 'refresh_token',
    USER: 'user',
    THEME: 'theme',
    SIDEBAR_COLLAPSED: 'sidebar_collapsed',
} as const;

// Date Formats
export const DATE_FORMATS = {
    SHORT: 'MMM dd, yyyy',
    LONG: 'MMMM dd, yyyy, h:mm a',
    ISO: "yyyy-MM-dd'T'HH:mm:ss",
} as const;

// WebSocket Events
export const WS_EVENTS = {
    CONNECTED: 'connected',
    DISCONNECTED: 'disconnected',
    ERROR: 'error',
    MESSAGE: 'message',
    SCAN_UPDATE: 'scan_update',
    THREAT_DETECTED: 'threat_detected',
    AGENT_STATUS_CHANGE: 'agent_status_change',
} as const;

// User Roles
export const USER_ROLES = {
    ADMIN: 'admin',
    USER: 'user',
    ANALYST: 'analyst',
    VIEWER: 'viewer',
} as const;

// Subscription Plans
export const SUBSCRIPTION_PLANS = {
    FREE: 'free',
    BASIC: 'basic',
    PRO: 'pro',
    ENTERPRISE: 'enterprise',
} as const;

// Toast Types
export const TOAST_TYPES = {
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info',
} as const;
