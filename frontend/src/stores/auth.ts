import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { message } from 'ant-design-vue'
import type { User } from '../types/models'
import { authService } from '../services/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const isLoading = ref(false)
  
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_admin || false)
  
  const initialize = async () => {
    if (token.value && !user.value) {
      try {
        await refreshUser()
      } catch (error) {
        logout()
      }
    }
  }
  
  const login = async (email: string, password: string) => {
    isLoading.value = true
    try {
      const response = await authService.login(email, password)
      token.value = response.token
      user.value = response.user
      localStorage.setItem('token', response.token)
      message.success('Login successful')
    } catch (error: any) {
      message.error(error.message || 'Login failed')
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  const register = async (email: string, password: string, name: string) => {
    isLoading.value = true
    try {
      const response = await authService.register(email, password, name)
      token.value = response.token
      user.value = response.user
      localStorage.setItem('token', response.token)
      message.success('Registration successful')
    } catch (error: any) {
      message.error(error.message || 'Registration failed')
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    message.success('Logged out successfully')
  }
  
  const refreshUser = async () => {
    if (!token.value) return
    
    try {
      const userData = await authService.getProfile()
      user.value = userData
    } catch (error) {
      throw new Error('Failed to refresh user data')
    }
  }
  
  const forgotPassword = async (email: string) => {
    try {
      await authService.forgotPassword(email)
      message.success('Password reset email sent')
    } catch (error: any) {
      message.error(error.message || 'Failed to send reset email')
      throw error
    }
  }
  
  const resetPassword = async (token: string, password: string) => {
    try {
      await authService.resetPassword(token, password)
      message.success('Password reset successful')
    } catch (error: any) {
      message.error(error.message || 'Failed to reset password')
      throw error
    }
  }
  
  return {
    user,
    token,
    isLoading,
    isAuthenticated,
    isAdmin,
    initialize,
    login,
    register,
    logout,
    refreshUser,
    forgotPassword,
    resetPassword
  }
})