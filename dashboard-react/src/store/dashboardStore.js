import { create } from 'zustand';

export const useDashboardStore = create((set) => ({
    stats: {
        teamAHealth: 98,
        teamBHealth: 97,
        nodesRunning: 200,
        avgLatency: 42,
        queueLoad: 11,
    },

    updateStats: (newStats) => set((state) => ({
        stats: { ...state.stats, ...newStats }
    })),

    logs: [],

    addLog: (log) => set((state) => ({
        logs: [log, ...state.logs].slice(0, 50) // Keep last 50 logs
    })),

    events: [],

    addEvent: (event) => set((state) => ({
        events: [event, ...state.events].slice(0, 20) // Keep last 20 events
    })),

    nodes: [
        { id: 'A1', x: 50, y: 50, status: 'healthy' },
        { id: 'A2', x: 200, y: 80, status: 'healthy' },
        { id: 'B1', x: 150, y: 150, status: 'slow' },
        { id: 'C1', x: 80, y: 220, status: 'healthy' },
        { id: 'C2', x: 280, y: 200, status: 'healthy' },
        { id: 'D1', x: 400, y: 100, status: 'healthy' },
        { id: 'D2', x: 450, y: 180, status: 'healthy' },
        { id: 'E1', x: 550, y: 50, status: 'healthy' },
    ],

    updateNodeStatus: (nodeId, status) => set((state) => ({
        nodes: state.nodes.map((node) =>
            node.id === nodeId ? { ...node, status } : node
        ),
    })),
}));
