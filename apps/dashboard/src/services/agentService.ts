/**
 * Agent Management Service
 * 
 * @created 2025-11-26
 */

import { api } from './api';

export interface Agent {
    id: number;
    name: string;
    description?: string;
    agent_type: string;
    status: 'active' | 'inactive' | 'error' | 'maintenance';
    configuration?: Record<string, any>;
    capabilities?: string[];
    metrics?: Record<string, any>;
    created_at: string;
    updated_at: string;
    last_active?: string;
}

export interface CreateAgentData {
    name: string;
    description?: string;
    agent_type: string;
    configuration?: Record<string, any>;
}

export interface UpdateAgentData {
    name?: string;
    description?: string;
    status?: string;
    configuration?: Record<string, any>;
}

class AgentService {
    /**
     * Get all agents
     */
    async getAgents(): Promise<Agent[]> {
        return api.get<Agent[]>('/agents');
    }

    /**
     * Get single agent by ID
     */
    async getAgent(id: number): Promise<Agent> {
        return api.get<Agent>(`/agents/${id}`);
    }

    /**
     * Create new agent
     */
    async createAgent(data: CreateAgentData): Promise<Agent> {
        return api.post<Agent>('/agents', data);
    }

    /**
     * Update agent
     */
    async updateAgent(id: number, data: UpdateAgentData): Promise<Agent> {
        return api.put<Agent>(`/agents/${id}`, data);
    }

    /**
     * Delete agent
     */
    async deleteAgent(id: number): Promise<void> {
        await api.delete(`/agents/${id}`);
    }

    /**
     * Start agent
     */
    async startAgent(id: number): Promise<Agent> {
        return api.post<Agent>(`/agents/${id}/start`);
    }

    /**
     * Stop agent
     */
    async stopAgent(id: number): Promise<Agent> {
        return api.post<Agent>(`/agents/${id}/stop`);
    }

    /**
     * Get agent metrics
     */
    async getAgentMetrics(id: number): Promise<Record<string, any>> {
        return api.get(`/agents/${id}/metrics`);
    }

    /**
     * Get agent logs
     */
    async getAgentLogs(id: number, limit: number = 100): Promise<any[]> {
        return api.get(`/agents/${id}/logs`, { params: { limit } });
    }
}

export const agentService = new AgentService();
export default agentService;
