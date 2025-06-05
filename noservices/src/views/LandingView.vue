<script setup lang="ts">
// Remove Navbar import
</script>

<template>
  <div class="landing-page">
    <!-- Remove Navbar component -->
    <div class="landing-hero">
      <h1>Selamat Datang di Inventory Management Dashboard</h1>
      <p>
        Kelola stok, pantau penjualan, dan tingkatkan efisiensi bisnis Anda dengan dashboard modern berbasis microservices.
      </p>
      <p>
        Silakan login untuk mulai menggunakan sistem.
      </p>
    </div>
  </div>
</template>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: linear-gradient(120deg, #f8fafc 0%, #e0f7fa 100%);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: flex-start;
}
.landing-hero {
  text-align: center;
  margin-top: 5rem;
}
.landing-hero h1 {
  font-size: 2.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.2rem;
}
.landing-hero p {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 1.2rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}
</style>
