import { configureStore } from '@reduxjs/toolkit';
import authSlice from './slices/authSlice';
import agentsSlice from './slices/agentsSlice';
import securitySlice from './slices/securitySlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    agents: agentsSlice,
    security: securitySlice,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;