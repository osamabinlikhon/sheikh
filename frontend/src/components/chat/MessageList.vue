<template>
  <div class="message-list">
    <div v-for="message in messages" :key="message.id" :class="['message', message.role]">
      <div class="avatar"></div>
      <div class="content">{{ message.content }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

interface Message {
  id: string;
  role: 'user' | 'agent';
  content: string;
}

defineProps<{
  messages: Message[];
}>();
</script>

<style scoped>
.message-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px;
  border-radius: 8px;
  background-color: #f0f0f0;
}

.message.user {
  justify-content: flex-end;
  background-color: #e6f7ff;
}

.message.agent {
  justify-content: flex-start;
  background-color: #f0f0f0;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #ccc;
  flex-shrink: 0;
}

.message.user .avatar {
  order: 2;
}

.content {
  flex-grow: 1;
}
</style>
