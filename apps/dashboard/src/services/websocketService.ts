/**
 * WebSocket Service
 * 
 * @created 2025-11-26
 */

type MessageHandler = (data: any) => void;
type EventHandlers = Map<string, Set<MessageHandler>>;

class WebSocketService {
    private ws: WebSocket | null = null;
    private url: string;
    private reconnectInterval: number = 5000;
    private reconnectTimer: NodeJS.Timeout | null = null;
    private eventHandlers: EventHandlers = new Map();
    private isConnecting: boolean = false;

    constructor() {
        this.url = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
    }

    /**
     * Connect to WebSocket server
     */
    connect(): void {
        if (this.ws?.readyState === WebSocket.OPEN || this.isConnecting) {
            console.log('[WS] Already connected or connecting');
            return;
        }

        this.isConnecting = true;
        const token = localStorage.getItem('access_token');
        const wsUrl = `${this.url}?token=${token}`;

        console.log('[WS] Connecting to', wsUrl);

        try {
            this.ws = new WebSocket(wsUrl);

            this.ws.onopen = () => {
                console.log('[WS] Connected');
                this.isConnecting = false;
                this.emit('connected', {});

                // Clear reconnect timer
                if (this.reconnectTimer) {
                    clearTimeout(this.reconnectTimer);
                    this.reconnectTimer = null;
                }
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log('[WS] Message received:', data);

                    // Emit to specific event handlers
                    if (data.type) {
                        this.emit(data.type, data.payload || data);
                    }

                    // Emit to all handlers
                    this.emit('message', data);
                } catch (error) {
                    console.error('[WS] Error parsing message:', error);
                }
            };

            this.ws.onerror = (error) => {
                console.error('[WS] Error:', error);
                this.emit('error', error);
            };

            this.ws.onclose = () => {
                console.log('[WS] Disconnected');
                this.isConnecting = false;
                this.ws = null;
                this.emit('disconnected', {});

                // Attempt to reconnect
                this.scheduleReconnect();
            };
        } catch (error) {
            console.error('[WS] Connection error:', error);
            this.isConnecting = false;
            this.scheduleReconnect();
        }
    }

    /**
     * Disconnect from WebSocket server
     */
    disconnect(): void {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }

        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }

    /**
     * Send message to server
     */
    send(type: string, payload: any): void {
        if (this.ws?.readyState === WebSocket.OPEN) {
            const message = JSON.stringify({ type, payload });
            this.ws.send(message);
            console.log('[WS] Message sent:', { type, payload });
        } else {
            console.warn('[WS] Not connected, cannot send message');
        }
    }

    /**
     * Subscribe to event
     */
    on(event: string, handler: MessageHandler): () => void {
        if (!this.eventHandlers.has(event)) {
            this.eventHandlers.set(event, new Set());
        }

        this.eventHandlers.get(event)!.add(handler);

        // Return unsubscribe function
        return () => this.off(event, handler);
    }

    /**
     * Unsubscribe from event
     */
    off(event: string, handler: MessageHandler): void {
        const handlers = this.eventHandlers.get(event);
        if (handlers) {
            handlers.delete(handler);
        }
    }

    /**
     * Emit event to handlers
     */
    private emit(event: string, data: any): void {
        const handlers = this.eventHandlers.get(event);
        if (handlers) {
            handlers.forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`[WS] Error in event handler for ${event}:`, error);
                }
            });
        }
    }

    /**
     * Schedule reconnection attempt
     */
    private scheduleReconnect(): void {
        if (this.reconnectTimer) return;

        console.log(`[WS] Reconnecting in ${this.reconnectInterval}ms`);
        this.reconnectTimer = setTimeout(() => {
            this.reconnectTimer = null;
            this.connect();
        }, this.reconnectInterval);
    }

    /**
     * Check connection status
     */
    isConnected(): boolean {
        return this.ws?.readyState === WebSocket.OPEN;
    }
}

export const websocketService = new WebSocketService();
export default websocketService;
