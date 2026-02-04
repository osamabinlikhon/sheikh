<template>
  <div class="browser-viewer">
    <iframe :src="url" frameborder="0"></iframe>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

defineProps<{
  url: string;
}>();
</script>

<style scoped>
.browser-viewer {
  width: 100%;
  height: 100%;
  border: 1px solid #ccc;
}

.browser-viewer iframe {
  width: 100%;
  height: 100%;
}
</style>
