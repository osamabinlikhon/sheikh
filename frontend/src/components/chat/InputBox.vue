<template>
  <div class="input-box">
    <input
      type="text"
      v-model="inputContent"
      @keyup.enter="sendMessage"
      :placeholder="placeholder"
    />
    <button @click="sendMessage" :disabled="!inputContent.trim()">Send</button>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps<{
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: 'send', content: string): void;
}>();

const inputContent = ref('');

const sendMessage = () => {
  if (inputContent.value.trim()) {
    emit('send', inputContent.value);
    inputContent.value = '';
  }
};
</script>

<style scoped>
.input-box {
  display: flex;
  padding: 10px;
  border-top: 1px solid #eee;
}

.input-box input {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
}

.input-box button {
  padding: 8px 15px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-box button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
}
</style>
