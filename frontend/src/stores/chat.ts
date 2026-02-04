import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { message } from 'ant-design-vue'
import type { Message } from '../types/models'
import { chatService } from '../services/chat'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const isStreaming = ref(false)
  const sessionId = ref('')
  
  const addMessage = (message: Message) => {
    messages.value.push(message)
  }
  
  const updateMessage = (messageId: string, updates: Partial<Message>) => {
    const index = messages.value.findIndex(m => m.id === messageId)
    if (index !== -1) {
      messages.value[index] = { ...messages.value[index], ...updates }
    }
  }
  
  const clearMessages = () => {
    messages.value = []
  }
  
  const initialize = async (session: string) => {
    sessionId.value = session
    try {
      // Load existing messages for session
      const existingMessages = await chatService.getMessages(session)
      messages.value = existingMessages
    } catch (error) {
      console.warn('Failed to load existing messages:', error)
    }
  }
  
  const sendMessage = async (content: string, session: string) => {
    if (!content.trim()) return
    
    isStreaming.value = true
    
    try {
      // Send message and get streaming response
      const response = await chatService.sendMessage(content, session)
      
      // Handle streaming response
      for await (const chunk of response) {
        if (chunk.type === 'plan') {
          addMessage({
            id: `plan-${Date.now()}`,
            content: chunk.content,
            role: 'assistant',
            type: 'plan',
            timestamp: new Date()
          })
        } else if (chunk.type === 'tool_execution') {
          addMessage({
            id: `tool-${Date.now()}`,
            content: `Tool: ${chunk.tool}\nResult: ${JSON.stringify(chunk.result)}`,
            role: 'assistant',
            type: 'tool',
            timestamp: new Date()
          })
        } else if (chunk.type === 'completion') {
          addMessage({
            id: `response-${Date.now()}`,
            content: chunk.content,
            role: 'assistant',
            type: 'response',
            timestamp: new Date()
          })
        }
      }
      
    } catch (error: any) {
      message.error(error.message || 'Failed to send message')
      throw error
    } finally {
      isStreaming.value = false
    }
  }
  
  const cleanup = () => {
    messages.value = []
    isStreaming.value = false
    sessionId.value = ''
  }
  
  return {
    messages,
    isStreaming,
    sessionId,
    addMessage,
    updateMessage,
    clearMessages,
    initialize,
    sendMessage,
    cleanup
  }
})