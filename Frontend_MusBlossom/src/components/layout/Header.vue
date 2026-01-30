<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">
        <img src="@/assets/images/LogoMus.png" alt="MusBlossom" class="logo-image" />
        <span class="logo-text">MusBlossom</span>
      </router-link>

      <div class="nav-links">
        <router-link to="/">Главная</router-link>
        <router-link to="/posts">Сообщество</router-link>
        <router-link to="/playlists">Плейлисты</router-link>
        <router-link to="/concerts">Концерты</router-link>
        <router-link to="/search">Поиск</router-link>
      </div>

      <div class="auth-section">
        <div v-if="!authStore.isAuthenticated" class="guest-buttons">
          <router-link to="/login" class="btn btn-login">Войти</router-link>
          <router-link to="/register" class="btn btn-register">Регистрация</router-link>
        </div>

        <div v-else class="user-menu">
          <router-link to="/profile" class="user-info">
            <img :src="userAvatar" class="user-avatar" alt="Avatar" />
            <span class="user-name">{{ userFullName }}</span>
          </router-link>
          <button @click="authStore.logout" class="btn btn-logout">Выйти</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Header',
  setup() {
    const authStore = useAuthStore()

    onMounted(() => {
      authStore.init()
      console.log('Header mounted, auth status:', authStore.isAuthenticated)
    })

    const userAvatar = computed(() => {
      const user = authStore.user
      if (user?.avatar_url) {
        return user.avatar_url
      }
      return new URL('@/assets/images/Avatar.jpg', import.meta.url).href
    })

    const userFullName = computed(() => {
      const user = authStore.user
      if (user?.username) {
        return user.username
      }
      return 'Пользователь'
    })

    const handleAuthChange = () => {
      console.log('Auth changed event received')
      authStore.syncWithLocalStorage()
    }

    onMounted(() => {
      window.addEventListener('auth-changed', handleAuthChange)
    })

    onUnmounted(() => {
      window.removeEventListener('auth-changed', handleAuthChange)
    })

    return {
      authStore,
      userAvatar,
      userFullName,
    }
  },
}
</script>

<style scoped>
.navbar {
  background: linear-gradient(90deg, #8a2be2 0%, #4b0082 100%);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  gap: 0.5rem;
}
.logo-image {
  width: 50px;
  height: 40px;
  object-fit: contain;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
}

.logo-icon {
  margin-left: 0.5rem;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-links a:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-links a.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.auth-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.guest-buttons {
  display: flex;
  gap: 0.5rem;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: white;
  transition: opacity 0.3s;
}

.user-info:hover {
  opacity: 0.9;
}

.user-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 500;
  max-width: 150px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Кнопки */
.btn {
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-login {
  background-color: transparent;
  color: white;
  border: 1px solid white;
}

.btn-login:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.btn-register {
  background-color: white;
  color: #8a2be2;
}

.btn-register:hover {
  background-color: #f0f0f0;
}

.btn-logout {
  background-color: #ff4757;
  color: white;
  padding: 0.5rem 1rem;
}

.btn-logout:hover {
  background-color: #ff3742;
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
  }

  .auth-section {
    width: 100%;
    justify-content: center;
  }

  .user-name {
    max-width: 100px;
  }
}
</style>
