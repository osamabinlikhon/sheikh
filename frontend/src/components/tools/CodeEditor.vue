<template>
  <div class="code-editor" ref="editorContainer"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import * as monaco from 'monaco-editor';

const props = defineProps<{
  modelValue: string;
  language: string;
  readOnly?: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const editorContainer = ref<HTMLElement | null>(null);
let editor: monaco.editor.IStandaloneCodeEditor | null = null;

onMounted(() => {
  if (editorContainer.value) {
    editor = monaco.editor.create(editorContainer.value, {
      value: props.modelValue,
      language: props.language,
      readOnly: props.readOnly,
      theme: 'vs-dark', // You can change the theme
      minimap: { enabled: false },
    });

    editor.onDidChangeModelContent(() => {
      if (editor) {
        emit('update:modelValue', editor.getValue());
      }
    });
  }
});

onBeforeUnmount(() => {
  if (editor) {
    editor.dispose();
  }
});

watch(
  () => props.modelValue,
  (newValue) => {
    if (editor && newValue !== editor.getValue()) {
      editor.setValue(newValue);
    }
  }
);

watch(
  () => props.language,
  (newLanguage) => {
    if (editor) {
      monaco.editor.setModelLanguage(editor.getModel()!, newLanguage);
    }
  }
);

watch(
  () => props.readOnly,
  (newReadOnly) => {
    if (editor) {
      editor.updateOptions({ readOnly: newReadOnly });
    }
  }
);
</script>

<style scoped>
.code-editor {
  width: 100%;
  height: 400px; /* Adjust height as needed */
  border: 1px solid #ccc;
}
</style>
