<template>
  <div class="tool-viewer">
    <h3>Tool Output:</h3>
    <pre>{{ JSON.stringify(output, null, 2) }}</pre>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

defineProps<{
  output: any;
}>();
</script>

<style scoped>
.tool-viewer {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 4px;
  margin-top: 10px;
}

.tool-viewer pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
