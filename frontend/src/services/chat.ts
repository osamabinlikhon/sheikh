import axios from 'axios'
import type { Message } from '../types/models'

export interface ChatResponse {
  type: 'plan' | 'tool_execution' | 'tool_error' | 'reflection' | 'completion'
  content?: string
  tool?: string
  arguments?: any
  result?: any
  error?: string
}

class ChatService {
  private api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    timeout: 30000,
  })

  async sendMessage(content: string, sessionId: string): Promise<AsyncGenerator<ChatResponse>> {
    const response = await this.api.post(
      '/api/v1/chat/send',
      { content, session_id: sessionId },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      }
    )

    // Return a generator that yields streaming responses
    return this.parseStreamResponse(response.data)
  }

  async getMessages(sessionId: string): Promise<Message[]> {
    try {
      const response = await this.api.get(`/api/v1/chat/messages/${sessionId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      return response.data.messages || []
    } catch (error) {
      console.warn('Failed to load messages:', error)
      return []
    }
  }

  async clearMessages(sessionId: string): Promise<void> {
    await this.api.delete(`/api/v1/chat/messages/${sessionId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
  }

  private async *parseStreamResponse(data: any): AsyncGenerator<ChatResponse> {
    // Handle different response formats
    if (Array.isArray(data)) {
      for (const item of data) {
        yield item
      }
    } else if (data && typeof data === 'object') {
      yield data
    }
  }
}

export const chatService = new ChatService()