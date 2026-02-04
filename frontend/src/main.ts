import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Assuming you'll create a router file
import { 
  Bubble, 
  Conversations, 
  Prompts, 
  Sender,
  useXAgent,
  useXChat
} from ' @ant-design/x';
import ' @ant-design/x/dist/index.css';

const app = createApp(App);

// Register Ant Design X components
app.component('Bubble', Bubble);
app.component('Conversations', Conversations);
app.component('Prompts', Prompts);
app.component('Sender', Sender);

app.use(router); // Use the router
app.mount('#app');
