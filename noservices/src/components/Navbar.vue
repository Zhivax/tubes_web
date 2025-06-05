<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userName = ref('')
const isLoggedIn = ref(false)

onMounted(() => {
  // Only check login callback if we have query params
  if (window.location.search.includes('access_token')) {
    handleLoginCallback()
  }
})

function handleLoginCallback() {
  const params = new URLSearchParams(window.location.search)
  const accessToken = params.get('access_token')
  const name = params.get('name')
  
  if (accessToken) {
    localStorage.setItem('access_token', accessToken)
    if (name) {
      localStorage.setItem('user_name', name)
      userName.value = name
    }
    isLoggedIn.value = true
    // Clean URL
    window.history.replaceState({}, document.title, window.location.pathname)
    router.push('/dashboard')
  }
}

function login() {
  // Clear existing session
  localStorage.clear()
  isLoggedIn.value = false
  userName.value = ''
  
  // Redirect to auth service
  window.location.href = 'http://localhost:5001/auth/login/google'
}

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_name')
  userName.value = ''
  isLoggedIn.value = false
  router.push('/')
}
</script>

<template>
  <nav class="navbar">
    <div class="navbar-user">
      <button class="user-btn" @click="isLoggedIn ? logout() : login()">
        {{ isLoggedIn ? `${userName} (Logout)` : 'Login with Google' }}
      </button>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  width: 100%;
  min-width: 100%;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  background: var(--color-background-soft);
  border-bottom: 1px solid var(--color-border);
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  position: relative;
  padding: 0 2rem;
  box-sizing: border-box;
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
