<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useXChat } from ' @ant-design/x';
import { Bubble, Sender } from ' @ant-design/x';
import { SSEClient } from ' @/services/sse';

const { messages, sendMessage } = useXChat();
const sseClient = ref<SSEClient | null>(null);

onMounted(() => {
  sseClient.value = new SSEClient('/api/chat/stream');
  sseClient.value.onMessage((data) => {
    // Handle streaming messages
    messages.value.push(data);
  });
});

const handleSend = async (content: string) => {
  await sendMessage(content);
};
</script>

<template>
  <div class="chat-interface">
    <Bubble 
      v-for="msg in messages" 
      :key="msg.id"
      :content="msg.content"
      :role="msg.role"
    />
    <Sender 
      @send="handleSend"
      placeholder="Ask Agent Sheikh anything..."
    />
  </div>
</template>
