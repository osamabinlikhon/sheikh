<template>
  <div class="file-manager">
    <h3>File Manager</h3>
    <input type="text" v-model="currentPath" placeholder="Enter path" />
    <button @click="listFiles">List Files</button>

    <ul>
      <li v-for="file in files" :key="file.name">
        {{ file.name }} ({{ file.type }})
        <button v-if="file.type === 'file'" @click="readFile(file.name)">Read</button>
      </li>
    </ul>

    <div v-if="fileContent">
      <h4>Content of {{ selectedFile }}:</h4>
      <pre>{{ fileContent }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const currentPath = ref('.');
const files = ref<{ name: string; type: string }[]>([]);
const fileContent = ref('');
const selectedFile = ref('');

const listFiles = async () => {
  // Placeholder for API call to list files
  files.value = [
    { name: 'example.txt', type: 'file' },
    { name: 'my_folder', type: 'directory' },
  ];
};

const readFile = async (fileName: string) => {
  // Placeholder for API call to read file
  selectedFile.value = fileName;
  fileContent.value = `Content of ${fileName} goes here.`;
};
</script>

<style scoped>
.file-manager {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
}
</style>
