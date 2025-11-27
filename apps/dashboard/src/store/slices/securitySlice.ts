import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface SecurityEvent {
  id: string;
  type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  timestamp: string;
  description: string;
  source: string;
  destination?: string;
  status: 'detected' | 'investigating' | 'remediated' | 'closed';
}

interface SecurityThreat {
  id: string;
  name: string;
  type: string;
  confidence: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  firstDetected: string;
  lastSeen: string;
  status: 'active' | 'quarantined' | 'blocked';
  targets: string[];
}

interface SecurityState {
  events: SecurityEvent[];
  threats: SecurityThreat[];
  stats: {
    totalEvents: number;
    criticalEvents: number;
    activeThreats: number;
    blockedRequests: number;
  };
  loading: boolean;
  error: string | null;
}

const initialState: SecurityState = {
  events: [],
  threats: [],
  stats: {
    totalEvents: 0,
    criticalEvents: 0,
    activeThreats: 0,
    blockedRequests: 0,
  },
  loading: false,
  error: null,
};

const securitySlice = createSlice({
  name: 'security',
  initialState,
  reducers: {
    fetchSecurityDataStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchSecurityDataSuccess: (
      state,
      action: PayloadAction<{
        events: SecurityEvent[];
        threats: SecurityThreat[];
        stats: SecurityState['stats'];
      }>
    ) => {
      state.events = action.payload.events;
      state.threats = action.payload.threats;
      state.stats = action.payload.stats;
      state.loading = false;
    },
    fetchSecurityDataFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    addSecurityEvent: (state, action: PayloadAction<SecurityEvent>) => {
      state.events.unshift(action.payload);
      if (action.payload.severity === 'critical') {
        state.stats.criticalEvents += 1;
      }
      state.stats.totalEvents += 1;
    },
    updateThreatStatus: (
      state,
      action: PayloadAction<{ id: string; status: SecurityThreat['status'] }>
    ) => {
      const threat = state.threats.find(t => t.id === action.payload.id);
      if (threat) {
        threat.status = action.payload.status;
      }
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const {
  fetchSecurityDataStart,
  fetchSecurityDataSuccess,
  fetchSecurityDataFailure,
  addSecurityEvent,
  updateThreatStatus,
  clearError,
} = securitySlice.actions;

export default securitySlice.reducer;