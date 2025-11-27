/**
 * Security Service
 * 
 * @created 2025-11-26
 */

import { api } from './api';
import { mockStats, isDevelopmentMode } from './mockAuth';

export interface SecurityScan {
    id: number;
    scan_name: string;
    target: string;
    scan_type: string;
    status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
    progress: number;
    started_at?: string;
    completed_at?: string;
    results?: Record<string, any>;
    summary?: string;
    created_at: string;
}

export interface CreateScanData {
    scan_name: string;
    target: string;
    scan_type: string;
    configuration?: Record<string, any>;
}

export interface Threat {
    id: number;
    threat_type: string;
    severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
    title: string;
    description?: string;
    source?: string;
    detected_at: string;
    mitigated: boolean;
}

export interface Vulnerability {
    id: number;
    cve_id?: string;
    title: string;
    description?: string;
    severity: 'critical' | 'high' | 'medium' | 'low';
    cvss_score?: number;
    status: string;
}

class SecurityService {
    /**
     * Get all scans
     */
    async getScans(page: number = 1, limit: number = 20): Promise<SecurityScan[]> {
        return api.get<SecurityScan[]>('/scans', { params: { page, limit } });
    }

    /**
     * Get single scan
     */
    async getScan(id: number): Promise<SecurityScan> {
        return api.get<SecurityScan>(`/scans/${id}`);
    }

    /**
     * Create new scan
     */
    async createScan(data: CreateScanData): Promise<SecurityScan> {
        return api.post<SecurityScan>('/scans', data);
    }

    /**
     * Cancel scan
     */
    async cancelScan(id: number): Promise<SecurityScan> {
        return api.post<SecurityScan>(`/scans/${id}/cancel`);
    }

    /**
     * Get scan threats
     */
    async getScanThreats(scanId: number): Promise<Threat[]> {
        return api.get<Threat[]>(`/scans/${scanId}/threats`);
    }

    /**
     * Get scan vulnerabilities
     */
    async getScanVulnerabilities(scanId: number): Promise<Vulnerability[]> {
        return api.get<Vulnerability[]>(`/scans/${scanId}/vulnerabilities`);
    }

    /**
   * Get security dashboard stats
   */
    async getSecurityStats(): Promise<Record<string, any>> {
        try {
            return await api.get('/security/stats');
        } catch (error) {
            if (isDevelopmentMode()) {
                console.warn('🎭 Using mock stats (backend not available)');
                return mockStats;
            }
            throw error;
        }
    }

    /**
     * Get threat trends
     */
    async getThreatTrends(days: number = 30): Promise<any[]> {
        return api.get('/security/trends', { params: { days } });
    }
}

export const securityService = new SecurityService();
export default securityService;
