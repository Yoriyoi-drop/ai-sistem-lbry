/**
 * Agents Management Hook
 * 
 * @created 2025-11-26
 */

import { useState, useEffect, useCallback } from 'react';
import { agentService, Agent, CreateAgentData, UpdateAgentData } from '../services';

export const useAgents = () => {
    const [agents, setAgents] = useState<Agent[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Fetch all agents
    const fetchAgents = useCallback(async () => {
        setLoading(true);
        setError(null);

        try {
            const data = await agentService.getAgents();
            setAgents(data);
            return data;
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || 'Failed to fetch agents';
            setError(errorMsg);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    // Create new agent
    const createAgent = useCallback(async (data: CreateAgentData) => {
        setLoading(true);
        setError(null);

        try {
            const newAgent = await agentService.createAgent(data);
            setAgents(prev => [...prev, newAgent]);
            return newAgent;
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || 'Failed to create agent';
            setError(errorMsg);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    // Update agent
    const updateAgent = useCallback(async (id: number, data: UpdateAgentData) => {
        setLoading(true);
        setError(null);

        try {
            const updatedAgent = await agentService.updateAgent(id, data);
            setAgents(prev => prev.map(agent =>
                agent.id === id ? updatedAgent : agent
            ));
            return updatedAgent;
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || 'Failed to update agent';
            setError(errorMsg);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    // Delete agent
    const deleteAgent = useCallback(async (id: number) => {
        setLoading(true);
        setError(null);

        try {
            await agentService.deleteAgent(id);
            setAgents(prev => prev.filter(agent => agent.id !== id));
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || 'Failed to delete agent';
            setError(errorMsg);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    // Start agent
    const startAgent = useCallback(async (id: number) => {
        try {
            const updatedAgent = await agentService.startAgent(id);
            setAgents(prev => prev.map(agent =>
                agent.id === id ? updatedAgent : agent
            ));
            return updatedAgent;
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || 'Failed to start agent';
            setError(errorMsg);
            throw err;
        }
    }, []);

    // Stop agent
    const stopAgent = useCallback(async (id: number) => {
        try {
            const updatedAgent = await agentService.stopAgent(id);
            setAgents(prev => prev.map(agent =>
                agent.id === id ? updatedAgent : agent
            ));
            return updatedAgent;
        } catch (err: any) {
            const errorMsg = err.response?.data?.detail || 'Failed to stop agent';
            setError(errorMsg);
            throw err;
        }
    }, []);

    // Load agents on mount
    useEffect(() => {
        fetchAgents();
    }, [fetchAgents]);

    return {
        agents,
        loading,
        error,
        fetchAgents,
        createAgent,
        updateAgent,
        deleteAgent,
        startAgent,
        stopAgent,
    };
};

export default useAgents;
