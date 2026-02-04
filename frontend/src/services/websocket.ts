import { ref } from 'vue';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

export function useWebSocket(sessionId: string) {
  const ws = ref<WebSocket | null>(null);
  const messages = ref<any[]>([]);
  const isConnected = ref(false);

  const connect = () => {
    ws.value = new WebSocket(`${WS_URL}/${sessionId}`);

    ws.value.onopen = () => {
      isConnected.value = true;
      console.log('WebSocket connected');
    };

    ws.value.onmessage = (event) => {
      messages.value.push(JSON.parse(event.data));
    };

    ws.value.onclose = () => {
      isConnected.value = false;
      console.log('WebSocket disconnected');
    };

    ws.value.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  };

  const send = (message: any) => {
    if (ws.value?.readyState === WebSocket.OPEN) {
      ws.value.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not open.');
    }
  };

  const disconnect = () => {
    if (ws.value) {
      ws.value.close();
    }
  };

  return {
    ws,
    messages,
    isConnected,
    connect,
    send,
    disconnect,
  };
}
