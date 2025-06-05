<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

const items = ref<any[]>([])
const loading = ref(false)
const error = ref('')
const showForm = ref(false)
const isEdit = ref(false)
const form = reactive({
  id: '',
  name: '',
  stock: 0,
  description: ''
})

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

function openAddForm() {
  isEdit.value = false
  form.id = ''
  form.name = ''
  form.stock = 0
  form.description = ''
  showForm.value = true
}

function openEditForm(item: any) {
  isEdit.value = true
  form.id = item.id || item._id || ''
  form.name = item.name
  form.stock = item.stock
  form.description = item.description || ''
  showForm.value = true
}

async function saveItem() {
  loading.value = true
  error.value = ''
  try {
    const url = `/api/inventory/${form.id || form.name.replace(/\s+/g, '-').toLowerCase()}`
    const method = isEdit.value ? 'POST' : 'POST'
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: form.name,
        stock: form.stock,
        description: form.description
      })
    })
    if (!res.ok) throw new Error('Failed to save item')
    showForm.value = false
    await fetchInventory()
  } catch (e) {
    error.value = 'Failed to save item'
  }
  loading.value = false
}

async function deleteItem(item: any) {
  if (!confirm('Delete this item?')) return
  loading.value = true
  error.value = ''
  try {
    const url = `/api/inventory/${item.id || item._id}`
    const res = await fetch(url, { method: 'DELETE' })
    if (!res.ok) throw new Error('Failed to delete item')
    await fetchInventory()
  } catch (e) {
    error.value = 'Failed to delete item'
  }
  loading.value = false
}

onMounted(fetchInventory)
</script>

<template>
  <div class="inventory-page">
    <h1>Inventory Management</h1>
    <div class="actions">
      <button @click="openAddForm">Add Item</button>
      <button @click="fetchInventory">Refresh</button>
    </div>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <table v-if="items.length && !loading" class="inventory-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Stock</th>
          <th>Description</th>
          <th style="width:120px">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id || item._id">
          <td>{{ item.name }}</td>
          <td>{{ item.stock }}</td>
          <td>{{ item.description }}</td>
          <td>
            <button @click="openEditForm(item)">Edit</button>
            <button @click="deleteItem(item)" class="danger">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="!items.length && !loading" class="empty">No items found.</div>

    <div v-if="showForm" class="modal">
      <div class="modal-content">
        <h2>{{ isEdit ? 'Edit Item' : 'Add Item' }}</h2>
        <form @submit.prevent="saveItem">
          <label>
            Name:
            <input v-model="form.name" required />
          </label>
          <label>
            Stock:
            <input type="number" v-model="form.stock" min="0" required />
          </label>
          <label>
            Description:
            <textarea v-model="form.description" />
          </label>
          <div class="modal-actions">
            <button type="submit">{{ isEdit ? 'Update' : 'Add' }}</button>
            <button type="button" @click="showForm = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.inventory-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
  box-sizing: border-box;
}

.inventory-page h1 {
  margin-bottom: 1.5rem;
}

.inventory-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  background: var(--color-background-soft);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.inventory-table th,
.inventory-table td {
  padding: 0.7rem 1rem;
  border-bottom: 1px solid var(--color-border);
  text-align: left;
}

.inventory-table th {
  background: var(--color-background-mute);
  font-weight: 600;
}

.inventory-table tr:last-child td {
  border-bottom: none;
}

.actions {
  margin-bottom: 1rem;
  text-align: center;
  margin-top: 2rem;
}

.actions button {
  margin-right: 0.7rem;
}

button.danger {
  background: #e74c3c;
  color: #fff;
}

button.danger:hover {
  background: #c0392b;
}

.empty {
  text-align: center;
  color: #888;
  margin: 2rem 0;
}

.error {
  color: #e74c3c;
  margin: 1rem 0;
  text-align: center;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--color-background);
  padding: 2rem 2.5rem;
  border-radius: 10px;
  min-width: 320px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
}

.modal-content h2 {
  margin-bottom: 1rem;
}

.modal-content label {
  display: block;
  margin-bottom: 1rem;
}

.modal-content input,
.modal-content textarea {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.3rem;
  border: 1px solid var(--color-border);
  border-radius: 5px;
  font-size: 1rem;
  background: var(--color-background-soft);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}
</style>
