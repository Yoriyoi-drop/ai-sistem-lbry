import { useState, useEffect, useRef } from 'react';

export const useWebSocket = (url, options = {}) => {
  const [ws, setWs] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  useEffect(() => {
    const connect = () => {
      const websocket = new WebSocket(url);

      websocket.onopen = (event) => {
        setIsConnected(true);
        if (options.onOpen) options.onOpen(event);
      };

      websocket.onmessage = (event) => {
        if (options.onMessage) options.onMessage(event);
      };

      websocket.onclose = (event) => {
        setIsConnected(false);
        if (options.onClose) options.onClose(event);
        
        // Attempt to reconnect after a delay
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
        }
        reconnectTimeoutRef.current = setTimeout(connect, 3000);
      };

      websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        if (options.onError) options.onError(error);
      };

      wsRef.current = websocket;
      setWs(websocket);
    };

    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [url]);

  const sendMessage = (message) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(message);
    } else {
      console.warn('WebSocket is not connected');
    }
  };

  return { ws, isConnected, sendMessage };
};