<script setup lang="ts">
import { ref } from 'vue'
const userName = ref('User Name')
</script>

<template>
  <nav class="navbar">
    <div class="navbar-user">
      <button class="user-btn">{{ userName }}</button>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  background: var(--color-background-soft);
  border-bottom: 1px solid var(--color-border);
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  position: sticky;
  top: 0;
  z-index: 30;
  padding: 0 2rem 0 0;
}

.navbar-user {
  margin-left: auto;
}

.user-btn {
  background: hsla(160, 100%, 37%, 0.12);
  color: var(--color-text);
  border: none;
  border-radius: 20px;
  padding: 0.5rem 1.2rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.user-btn:hover {
  background: hsla(160, 100%, 37%, 0.22);
}
</style>
