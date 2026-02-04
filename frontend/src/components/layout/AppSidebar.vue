<template>
  <aside class="app-sidebar">
    <div class="sidebar-header">
      <h3>Sessions</h3>
      <button @click="createNewSession">+</button>
    </div>
    <ul class="session-list">
      <li v-for="session in sessions" :key="session.id" @click="selectSession(session.id)" :class="{ active: session.id === activeSessionId }">
        {{ session.name || `Session ${session.id.substring(0, 4)}...` }}
      </li>
    </ul>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Session {
  id: string;
  name?: string;
}

const sessions = ref<Session[]>([
  { id: '1', name: 'Initial Chat' },
  { id: '2', name: 'Bug Fixing' },
]);
const activeSessionId = ref('1');

const createNewSession = () => {
  const newSessionId = String(Math.random()).substring(2, 6);
  sessions.value.push({ id: newSessionId });
  activeSessionId.value = newSessionId;
};

const selectSession = (id: string) => {
  activeSessionId.value = id;
  // In a real app, this would load the session's conversation history
};
</script>

<style scoped>
.app-sidebar {
  width: 200px;
  background-color: #f0f2f5;
  padding: 10px;
  border-right: 1px solid #e8e8e8;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.sidebar-header button {
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
}

.session-list {
  list-style: none;
  padding: 0;
}

.session-list li {
  padding: 8px 5px;
  cursor: pointer;
  border-radius: 4px;
  margin-bottom: 5px;
}

.session-list li:hover {
  background-color: #e6f7ff;
}

.session-list li.active {
  background-color: #bae7ff;
  font-weight: bold;
}
</style>
