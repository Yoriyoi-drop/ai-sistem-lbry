/**
 * WebSocket Connection Hook
 * 
 * @created 2025-11-26
 */

import { useEffect, useCallback, useRef } from 'react';
import { websocketService } from '../services';

type MessageHandler = (data: any) => void;

export const useWebSocket = () => {
    const handlersRef = useRef<Map<string, MessageHandler>>(new Map());

    // Connect on mount
    useEffect(() => {
        websocketService.connect();

        return () => {
            websocketService.disconnect();
        };
    }, []);

    // Subscribe to event
    const on = useCallback((event: string, handler: MessageHandler) => {
        const unsubscribe = websocketService.on(event, handler);
        handlersRef.current.set(event, handler);

        return () => {
            unsubscribe();
            handlersRef.current.delete(event);
        };
    }, []);

    // Send message
    const send = useCallback((type: string, payload: any) => {
        websocketService.send(type, payload);
    }, []);

    // Check connection status
    const isConnected = useCallback(() => {
        return websocketService.isConnected();
    }, []);

    return {
        on,
        send,
        isConnected,
    };
};

export default useWebSocket;
