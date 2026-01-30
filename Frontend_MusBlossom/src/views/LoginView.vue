<template>
  <div class="login-view">
    <div class="login-container">
      <div class="login-left">
        <div class="login-header">
          <h1>Вход в аккаунт</h1>
          <p>Введите пароль и логин для входа</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              placeholder="your@email.com"
              required
              :disabled="loading"
            />
          </div>

          <div class="form-group">
            <label for="password">Пароль</label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              placeholder="••••••••"
              required
              :disabled="loading"
            />
          </div>

          <!-- Сообщение об ошибке -->
          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <button type="submit" class="btn-login" :disabled="loading">
            {{ loading ? 'Вход...' : 'Войти' }}
          </button>

          <div class="login-footer">
            <p>Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link></p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'LoginView',

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const form = ref({
      email: '',
      password: '',
    })

    const loading = ref(false)
    const error = ref(null)

    const handleLogin = async () => {
      loading.value = true
      error.value = null

      try {
        const result = await authStore.login(form.value.email, form.value.password)

        if (result.success) {
          console.log('Login successful, redirecting...')
          // Хедер должен автоматически обновиться через событие 'auth-changed'
          // которое отправляется в authStore.login()
          router.push('/')
        } else {
          error.value = result.error || 'Ошибка входа'
        }
      } catch (err) {
        console.error('Login error:', err)
        error.value = 'Ошибка соединения с сервером'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      error,
      handleLogin,
    }
  },
}
</script>

<style scoped>
.login-view {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-container {
  max-width: 450px;
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-left {
  padding: 3rem;
  background: rgba(255, 255, 255, 0.02);
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
  width: 100%;
}

.login-header h1 {
  font-size: 2.5rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #b0b0b0;
}

.login-form {
  max-width: 400px;
  width: 100%;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: white;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #8a2be2;
  background: rgba(255, 255, 255, 0.12);
}

.form-group input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Стиль для сообщения об ошибке */
.error-message {
  background: rgba(255, 71, 87, 0.1);
  border: 1px solid rgba(255, 71, 87, 0.3);
  color: #ff4757;
  padding: 0.8rem;
  border-radius: 8px;
  margin: 1rem 0;
  text-align: center;
  font-size: 0.9rem;
}

.btn-login {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 1rem;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.btn-login:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  margin-top: 2rem;
  color: #b0b0b0;
  width: 100%;
}

.login-footer a {
  color: #8a2be2;
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-left {
    padding: 2rem 1.5rem;
  }

  .login-container {
    max-width: 95%;
  }
}
</style>
