<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <img src="@/assets/logo.svg" alt="Logo" class="sidebar-logo" />
      <span class="sidebar-title">Inventory</span>
    </div>
    <nav class="sidebar-links">
      <RouterLink to="/" exact-active-class="active">Dashboard</RouterLink>
      <RouterLink to="/inventory" exact-active-class="active">Inventory</RouterLink>
      <RouterLink to="/about" exact-active-class="active">About</RouterLink>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 220px;
  background: var(--color-background-soft);
  border-right: 1px solid var(--color-border);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0;
  position: relative;
  top: 0;
  left: 0;
  z-index: 20;
}

.sidebar-brand {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 3rem;
  margin-bottom: 2rem;
  width: 100%;
}

.sidebar-logo {
  width: 48px;
  height: 48px;
  margin-bottom: 0.5rem;
}

.sidebar-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--color-heading);
  letter-spacing: 1px;
  text-align: center;
}

.sidebar-links {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  width: 100%;
  padding: 0 1rem;
}

.sidebar-links a {
  color: var(--color-text);
  font-weight: 500;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background 0.2s, color 0.2s;
  width: 100%;
  display: block;
}

.sidebar-links a.active,
.sidebar-links a:hover {
  background: hsla(160, 100%, 37%, 0.12);
  color: hsla(160, 100%, 37%, 1);
}

@media (max-width: 900px) {
  .sidebar {
    width: 60px;
  }
  .sidebar-brand {
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
  .sidebar-logo {
    width: 32px;
    height: 32px;
  }
  .sidebar-title {
    display: none;
  }
  .sidebar-links {
    padding: 0 0.3rem;
  }
  .sidebar-links a {
    padding: 0.5rem 0.5rem;
    font-size: 0.95rem;
    text-align: center;
  }
}
</style>
