import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useInventoryStore = defineStore('inventory', () => {
  const items = ref<any[]>([])
  const loading = ref(false)
  const error = ref('')

  async function fetchInventory() {
    loading.value = true
    error.value = ''
    try {
      const res = await fetch('/api/inventory')
      items.value = await res.json()
    } catch (e) {
      error.value = 'Failed to fetch inventory'
    }
    loading.value = false
  }

  return { items, loading, error, fetchInventory }
})
