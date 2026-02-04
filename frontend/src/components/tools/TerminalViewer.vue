<template>
  <div class="terminal-viewer" ref="terminalContainer"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

const terminalContainer = ref<HTMLElement | null>(null);
let term: Terminal | null = null;
let fitAddon: FitAddon | null = null;

onMounted(() => {
  if (terminalContainer.value) {
    term = new Terminal();
    fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.open(terminalContainer.value);
    fitAddon.fit();

    // Example: write some text to the terminal
    term.write('Welcome to the Agent Sheikh Terminal!\r\n');
    term.write('$ ');

    // Handle resize
    window.addEventListener('resize', handleResize);
  }
});

onBeforeUnmount(() => {
  if (term) {
    term.dispose();
  }
  window.removeEventListener('resize', handleResize);
});

const handleResize = () => {
  fitAddon?.fit();
};

// Expose a method to write to the terminal from parent component
const write = (text: string) => {
  term?.write(text);
};

defineExpose({ write });
</script>

<style scoped>
.terminal-viewer {
  width: 100%;
  height: 300px; /* Adjust height as needed */
  background-color: #000;
  color: #fff;
}
</style>
