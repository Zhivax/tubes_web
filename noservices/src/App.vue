<script setup lang="ts">
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="main-layout">
    <div class="layout-row">
      <Sidebar />
      <div class="content-col">
        <Navbar />
        <main class="main-content">
          <RouterView />
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
#main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.layout-row {
  display: flex;
  flex: 1;
  min-height: 0;
}

.content-col {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  min-height: 100vh;
  background: var(--color-background);
}

.main-content {
  flex: 1;
  padding: 2rem 0;
  width: 100%;
  box-sizing: border-box;
}
</style>
