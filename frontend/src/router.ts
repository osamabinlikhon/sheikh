import { createRouter, createWebHistory } from 'vue-router';
import ChatInterface from './components/chat/ChatInterface.vue';

const routes = [
  {
    path: '/',
    name: 'Chat',
    component: ChatInterface,
  },
  // Add other routes here if needed
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
