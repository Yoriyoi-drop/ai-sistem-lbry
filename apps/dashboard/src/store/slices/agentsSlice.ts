import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Agent {
  id: string;
  name: string;
  status: 'online' | 'offline' | 'busy';
  lastSeen: string;
  cpuUsage: number;
  memoryUsage: number;
  tasksCompleted: number;
  activeTasks: number;
  type: string; // team_a, team_b, team_c, etc.
}

interface AgentsState {
  agents: Agent[];
  selectedAgent: Agent | null;
  loading: boolean;
  error: string | null;
}

const initialState: AgentsState = {
  agents: [],
  selectedAgent: null,
  loading: false,
  error: null,
};

const agentsSlice = createSlice({
  name: 'agents',
  initialState,
  reducers: {
    fetchAgentsStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchAgentsSuccess: (state, action: PayloadAction<Agent[]>) => {
      state.agents = action.payload;
      state.loading = false;
    },
    fetchAgentsFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    setSelectedAgent: (state, action: PayloadAction<Agent>) => {
      state.selectedAgent = action.payload;
    },
    updateAgentStatus: (state, action: PayloadAction<{ id: string; status: Agent['status'] }>) => {
      const agent = state.agents.find(a => a.id === action.payload.id);
      if (agent) {
        agent.status = action.payload.status;
      }
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const { 
  fetchAgentsStart, 
  fetchAgentsSuccess, 
  fetchAgentsFailure, 
  setSelectedAgent, 
  updateAgentStatus,
  clearError 
} = agentsSlice.actions;

export default agentsSlice.reducer;