<template>
  <header class="app-header">
    <div class="logo">Agent Sheikh</div>
    <nav>
      <router-link to="/">Chat</router-link>
      <router-link to="/settings">Settings</router-link>
    </nav>
  </header>
</template>

<script setup lang="ts"></script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #f8f8f8;
  border-bottom: 1px solid #eee;
}

.logo {
  font-size: 24px;
  font-weight: bold;
}

nav a {
  margin-left: 20px;
  text-decoration: none;
  color: #333;
}

nav a:hover {
  color: #1890ff;
}
</style>
