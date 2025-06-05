<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const inventoryStats = ref({ total_items: 0, low_stock_items: 0, out_of_stock: 0 })
const salesStats = ref({ daily_sales: 0, weekly_sales: 0, monthly_sales: 0 })
const loading = ref(true)
const router = useRouter()

async function fetchStats() {
  loading.value = true
  try {
    const [inventoryRes, salesRes] = await Promise.all([
      fetch('/api/analytics/inventory').then((r) => r.json()),
      fetch('/api/analytics/sales').then((r) => r.json()),
    ])
    inventoryStats.value = inventoryRes
    salesStats.value = salesRes
  } catch (e) {
    // handle error
  }
  loading.value = false
}

onMounted(fetchStats)

function goToInventory() {
  router.push('/inventory')
}
</script>

<template>
  <div class="dashboard">
    <h1>Inventory Management Dashboard</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="stats-grid">
      <div class="stat-card">
        <h2>Total Items</h2>
        <p>{{ inventoryStats.total_items }}</p>
      </div>
      <div class="stat-card">
        <h2>Low Stock</h2>
        <p>{{ inventoryStats.low_stock_items }}</p>
      </div>
      <div class="stat-card">
        <h2>Out of Stock</h2>
        <p>{{ inventoryStats.out_of_stock }}</p>
      </div>
      <div class="stat-card">
        <h2>Daily Sales</h2>
        <p>{{ salesStats.daily_sales }}</p>
      </div>
      <div class="stat-card">
        <h2>Weekly Sales</h2>
        <p>{{ salesStats.weekly_sales }}</p>
      </div>
      <div class="stat-card">
        <h2>Monthly Sales</h2>
        <p>{{ salesStats.monthly_sales }}</p>
      </div>
    </div>
    <div class="actions">
      <button @click="goToInventory">Manage Inventory</button>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
  box-sizing: border-box;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.stat-card {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.stat-card h2 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.stat-card p {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
}

.actions {
  text-align: center;
  margin-top: 2rem;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #888;
  margin: 2rem 0;
}
</style>
