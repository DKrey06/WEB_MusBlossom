import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const user = ref(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)
  const error = ref(null)

  const init = () => {
    const token = localStorage.getItem('access_token')
    const userData = localStorage.getItem('user')
    if (token && userData) {
      try {
        user.value = JSON.parse(userData)
        isAuthenticated.value = true
        console.log('User restored from localStorage:', user.value?.username)
      } catch (e) {
        console.error('Error parsing user data:', e)
        clearAuthData()
      }
    }
  }

  const clearAuthData = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    user.value = null
    isAuthenticated.value = false
  }

  const register = async (username, email, password, bio = '') => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('http://localhost:5000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password, bio }),
      })

      const data = await response.json()
      console.log('Register response:', data)

      if (data.success) {
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('refresh_token', data.refresh_token)
        localStorage.setItem('user', JSON.stringify(data.user))

        user.value = data.user
        isAuthenticated.value = true

        window.dispatchEvent(new CustomEvent('auth-changed'))

        router.push({ path: '/', replace: true })
        return { success: true, user: data.user }
      } else {
        error.value = data.errors || data.error || 'Ошибка регистрации'
        return { success: false, error: error.value }
      }
    } catch (err) {
      console.error('Register error:', err)
      error.value = 'Ошибка соединения с сервером'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const login = async (email, password) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()
      console.log('Login response:', data)

      if (data.success) {
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('refresh_token', data.refresh_token)
        localStorage.setItem('user', JSON.stringify(data.user))

        user.value = data.user
        isAuthenticated.value = true

        window.dispatchEvent(new CustomEvent('auth-changed'))

        router.push({ path: '/', replace: true })
        return { success: true, user: data.user }
      } else {
        error.value = data.error || 'Ошибка входа'
        return { success: false, error: error.value }
      }
    } catch (err) {
      console.error('Login error:', err)
      error.value = 'Ошибка соединения с сервером'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    clearAuthData()
    window.dispatchEvent(new CustomEvent('auth-changed'))
    router.push('/login')
  }

  const refreshToken = async () => {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      console.log('No refresh token available')
      return false
    }

    try {
      const response = await fetch('http://localhost:5000/api/auth/refresh', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${refreshToken}`,
        },
      })

      const data = await response.json()
      console.log('Refresh token response:', data)

      if (data.success) {
        localStorage.setItem('access_token', data.access_token)
        return true
      } else {
        clearAuthData()
        return false
      }
    } catch (err) {
      console.error('Token refresh error:', err)
      clearAuthData()
      return false
    }
  }

  const fetchCurrentUser = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) return null

    try {
      const response = await fetch('http://localhost:5000/api/auth/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()
      if (data.success) {
        user.value = data.user
        localStorage.setItem('user', JSON.stringify(data.user))
        return data.user
      } else {
        clearAuthData()
        return null
      }
    } catch (err) {
      console.error('Fetch user error:', err)
      return null
    }
  }

  const syncWithLocalStorage = () => {
    const token = localStorage.getItem('access_token')
    const userData = localStorage.getItem('user')

    if (token && userData) {
      try {
        user.value = JSON.parse(userData)
        isAuthenticated.value = true
      } catch (e) {
        user.value = null
        isAuthenticated.value = false
      }
    } else {
      user.value = null
      isAuthenticated.value = false
    }
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    init,
    register,
    login,
    logout,
    refreshToken,
    fetchCurrentUser,
    syncWithLocalStorage,
    clearAuthData,
  }
})
