<template>
  <div class="register-view">
    <div class="register-container">
      <div class="register-header">
        <h1>Создать аккаунт</h1>
        <p>Присоединяйся к музыкальному сообществу</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-row">
          <div class="form-group">
            <label for="username">Имя пользователя *</label>
            <input
              type="text"
              id="username"
              v-model="form.username"
              placeholder="musiclover"
              required
              :disabled="loading"
              :class="{ error: errors.username }"
            />
            <div v-if="errors.username" class="error-message">{{ errors.username }}</div>
          </div>

          <div class="form-group">
            <label for="email">Email *</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              placeholder="your@email.com"
              required
              :disabled="loading"
              :class="{ error: errors.email }"
            />
            <div v-if="errors.email" class="error-message">{{ errors.email }}</div>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="password">Пароль *</label>
            <div class="password-input-wrapper">
              <input
                :type="showPassword ? 'text' : 'password'"
                id="password"
                v-model="form.password"
                placeholder="••••••••"
                required
                :disabled="loading"
                :class="{ error: errors.password }"
              />
              <button
                type="button"
                class="toggle-password"
                @click="showPassword = !showPassword"
                :title="showPassword ? 'Скрыть пароль' : 'Показать пароль'"
              >
                {{ showPassword ? 'Скрыть' : 'Показать' }}
              </button>
            </div>
            <div class="password-strength" :class="passwordStrengthClass">
              Сложность: {{ passwordStrength }}
            </div>
          </div>

          <div class="form-group">
            <label for="confirmPassword">Подтверждение пароля *</label>
            <div class="password-input-wrapper">
              <input
                :type="showConfirmPassword ? 'text' : 'password'"
                id="confirmPassword"
                v-model="form.confirmPassword"
                placeholder="••••••••"
                required
                :disabled="loading"
                :class="{ error: errors.confirmPassword }"
              />
              <button
                type="button"
                class="toggle-password"
                @click="showConfirmPassword = !showConfirmPassword"
                :title="showConfirmPassword ? 'Скрыть пароль' : 'Показать пароль'"
              >
                {{ showConfirmPassword ? 'Скрыть' : 'Показать' }}
              </button>
            </div>
            <div v-if="errors.confirmPassword" class="error-message">
              {{ errors.confirmPassword }}
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="bio">О себе</label>
          <textarea
            id="bio"
            v-model="form.bio"
            placeholder="Расскажи о своих музыкальных предпочтениях..."
            rows="3"
            maxlength="200"
            :disabled="loading"
          ></textarea>
          <div class="char-counter">{{ form.bio.length }}/200</div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-register" :disabled="loading">
            {{ loading ? 'Регистрация...' : 'Создать аккаунт' }}
          </button>

          <div class="login-link">
            Уже есть аккаунт? <router-link to="/login">Войти</router-link>
          </div>
        </div>

        <div v-if="authStore.error" class="error-alert">
          {{ authStore.error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'RegisterView',

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const form = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      bio: '',
    })

    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    const errors = ref({})
    const loading = computed(() => authStore.isLoading)

    const passwordStrength = computed(() => {
      const password = form.value.password
      if (!password) return 'Нет'

      let score = 0
      if (password.length >= 8) score++
      if (/[A-Z]/.test(password)) score++
      if (/[0-9]/.test(password)) score++
      if (/[^A-Za-z0-9]/.test(password)) score++

      const strengths = ['Слабый', 'Средний', 'Хороший', 'Надёжный']
      return strengths[Math.min(score - 1, 3)] || 'Слабый'
    })

    const passwordStrengthClass = computed(() => ({
      weak: passwordStrength.value === 'Слабый',
      medium: passwordStrength.value === 'Средний',
      good: passwordStrength.value === 'Хороший',
      strong: passwordStrength.value === 'Надёжный',
    }))

    const validateForm = () => {
      errors.value = {}

      if (!form.value.username) {
        errors.value.username = 'Имя пользователя обязательно'
      } else if (form.value.username.length < 3) {
        errors.value.username = 'Минимум 3 символа'
      }

      if (!form.value.email) {
        errors.value.email = 'Email обязателен'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
        errors.value.email = 'Некорректный email'
      }

      if (!form.value.password) {
        errors.value.password = 'Пароль обязателен'
      } else if (form.value.password.length < 6) {
        errors.value.password = 'Минимум 6 символов'
      }

      if (form.value.password !== form.value.confirmPassword) {
        errors.value.confirmPassword = 'Пароли не совпадают'
      }

      return Object.keys(errors.value).length === 0
    }

    const handleRegister = async () => {
      if (!validateForm()) {
        return
      }

      const result = await authStore.register(
        form.value.username,
        form.value.email,
        form.value.password,
        form.value.bio,
      )

      if (result.success) {
        console.log('Registration successful, redirecting...')
        router.push('/')
      }
    }

    onUnmounted(() => {
      if (authStore.error) {
        authStore.error = null
      }
    })

    return {
      form,
      showPassword,
      showConfirmPassword,
      errors,
      loading,
      authStore,
      passwordStrength,
      passwordStrengthClass,
      handleRegister,
    }
  },
}
</script>

<style scoped>
.register-view {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.register-container {
  max-width: 800px;
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h1 {
  font-size: 2.5rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.register-header p {
  color: #b0b0b0;
}

.register-form {
  margin-bottom: 3rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
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

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #8a2be2;
  background: rgba(255, 255, 255, 0.12);
}

.form-group input:disabled,
.form-group textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-group input.error,
.form-group textarea.error {
  border-color: #ff4757;
}

.password-input-wrapper {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid #444;
  border-radius: 5px;
  color: #b0b0b0;
  padding: 0.3rem 0.6rem;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.toggle-password:hover {
  background: rgba(138, 43, 226, 0.2);
  color: white;
}

.error-message {
  color: #ff4757;
  font-size: 0.9rem;
  margin-top: 0.3rem;
}

.password-strength {
  font-size: 0.9rem;
  margin-top: 0.3rem;
  padding: 0.2rem 0.5rem;
  border-radius: 5px;
  display: inline-block;
}

.password-strength.weak {
  color: #ff4757;
  background: rgba(255, 71, 87, 0.1);
}

.password-strength.medium {
  color: #ffa502;
  background: rgba(255, 165, 2, 0.1);
}

.password-strength.good {
  color: #2ed573;
  background: rgba(46, 213, 115, 0.1);
}

.password-strength.strong {
  color: #1e90ff;
  background: rgba(30, 144, 255, 0.1);
}

.char-counter {
  text-align: right;
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.3rem;
}

.form-actions {
  text-align: center;
}

.btn-register {
  padding: 1rem 3rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 1rem;
}

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.btn-register:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-link {
  color: #b0b0b0;
}

.login-link a {
  color: #8a2be2;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

.error-alert {
  background: rgba(255, 71, 87, 0.1);
  border: 1px solid #ff4757;
  color: #ff4757;
  padding: 1rem;
  border-radius: 10px;
  margin-top: 1rem;
  text-align: center;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .register-container {
    padding: 2rem 1rem;
  }
}
</style>
