<template>
  <div id="app">
    <AppHeader />
    <div class="main-content">
      <AppSidebar />
      <router-view />
    </div>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import AppHeader from './components/layout/AppHeader.vue';
import AppSidebar from './components/layout/AppSidebar.vue';
import AppFooter from './components/layout/AppFooter.vue';
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  display: flex;
  flex: 1;
}
</style>
