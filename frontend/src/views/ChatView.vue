<template>
  <div class="chat-container">
    <div class="chat-header">
      <h1>{{ $t('chat.title') }}</h1>
      <div class="header-actions">
        <a-button @click="clearChat" type="default">
          {{ $t('chat.clear') }}
        </a-button>
        <a-button @click="exportChat" type="default">
          {{ $t('chat.export') }}
        </a-button>
      </div>
    </div>
    
    <div class="chat-content">
      <div class="message-list" ref="messageList">
        <Bubble
          v-for="message in messages"
          :key="message.id"
          :content="message.content"
          :role="message.role"
          :loading="message.loading"
        />
        
        <div v-if="isTyping" class="typing-indicator">
          <a-spin size="small" />
          <span>{{ $t('chat.typing') }}</span>
        </div>
      </div>
      
      <div class="input-area">
        <Sender
          :placeholder="$t('chat.placeholder')"
          :disabled="isTyping"
          @send="sendMessage"
        />
      </div>
    </div>
    
    <div v-if="showTools" class="tools-panel">
      <a-tabs v-model:activeKey="activeTool">
        <a-tab-pane key="browser" :tab="$t('tools.browser')">
          <BrowserViewer :session-id="sessionId" />
        </a-tab-pane>
        <a-tab-pane key="terminal" :tab="$t('tools.terminal')">
          <TerminalViewer :session-id="sessionId" />
        </a-tab-pane>
        <a-tab-pane key="files" :tab="$t('tools.files')">
          <FileManager :session-id="sessionId" />
        </a-tab-pane>
      </a-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { useChatStore } from '../stores/chat'
import { useAuthStore } from '../stores/auth'
import { Sender, Bubble } from '@ant-design/x'
import BrowserViewer from '../components/tools/BrowserViewer.vue'
import TerminalViewer from '../components/tools/TerminalViewer.vue'
import FileManager from '../components/tools/FileManager.vue'

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()
const authStore = useAuthStore()

const messageList = ref<HTMLElement>()
const isTyping = ref(false)
const showTools = ref(false)
const activeTool = ref('browser')
const sessionId = ref('')

// Computed properties
const messages = computed(() => chatStore.messages)

// Methods
const sendMessage = async (content: string) => {
  if (!content.trim() || isTyping.value) return
  
  try {
    isTyping.value = true
    showTools.value = true
    
    // Add user message
    chatStore.addMessage({
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date()
    })
    
    // Send to agent
    await chatStore.sendMessage(content, sessionId.value)
    
  } catch (error: any) {
    message.error(error.message || 'Failed to send message')
  } finally {
    isTyping.value = false
  }
}

const clearChat = () => {
  chatStore.clearMessages()
  message.success('Chat cleared')
}

const exportChat = () => {
  const chatData = {
    session: sessionId.value,
    messages: chatStore.messages,
    exportedAt: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(chatData, null, 2)], {
    type: 'application/json'
  })
  
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `chat-${sessionId.value}-${Date.now()}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const scrollToBottom = async () => {
  await nextTick()
  if (messageList.value) {
    messageList.value.scrollTop = messageList.value.scrollHeight
  }
}

// Lifecycle hooks
onMounted(async () => {
  // Generate session ID if not exists
  if (!sessionId.value) {
    sessionId.value = `session-${Date.now()}`
  }
  
  // Initialize chat store
  await chatStore.initialize(sessionId.value)
  
  // Scroll to bottom when messages change
  scrollToBottom()
})

onUnmounted(() => {
  chatStore.cleanup()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--bg-color);
}

.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--card-bg);
}

.chat-header h1 {
  margin: 0;
  font-size: 20px;
  color: var(--text-color);
}

.header-actions {
  display: flex;
  gap: 8px;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  color: var(--text-secondary-color);
  font-size: 14px;
}

.input-area {
  padding: 16px;
  border-top: 1px solid var(--border-color);
  background-color: var(--card-bg);
}

.tools-panel {
  height: 400px;
  border-top: 1px solid var(--border-color);
  background-color: var(--card-bg);
  display: flex;
  flex-direction: column;
}

.tools-panel :deep(.ant-tabs) {
  height: 100%;
}

.tools-panel :deep(.ant-tabs-content-holder) {
  flex: 1;
  overflow: hidden;
}

.tools-panel :deep(.ant-tabs-tabpane) {
  height: 100%;
  overflow: auto;
}
</style>