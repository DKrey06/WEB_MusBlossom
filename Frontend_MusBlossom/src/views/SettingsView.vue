<template>
  <div class="settings-view">
    <div class="settings-header">
      <h1>Настройки</h1>
      <p>Управление вашим аккаунтом MusBlossom</p>
    </div>

    <div class="settings-container">
      <div class="settings-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="settings-content">
        <div v-if="activeTab === 'profile'" class="tab-content">
          <h2>Настройки профиля</h2>
          <form @submit.prevent="updateProfile" class="settings-form">
            <div class="form-group">
              <label for="username">Имя пользователя</label>
              <input id="username" v-model="profileForm.username" disabled class="form-control" />
              <small class="form-text">Имя пользователя нельзя изменить</small>
            </div>

            <div class="form-group">
              <label for="bio">О себе</label>
              <textarea
                id="bio"
                v-model="profileForm.bio"
                rows="3"
                class="form-control"
                placeholder="Расскажите о своих музыкальных предпочтениях..."
              ></textarea>
            </div>

            <div class="form-group">
              <label for="location">Местоположение</label>
              <input
                id="location"
                v-model="profileForm.location"
                class="form-control"
                placeholder="Город, страна"
              />
            </div>

            <div class="form-group">
              <label>Любимые жанры</label>
              <p class="form-hint">Выберите до 5 любимых жанров</p>
              <div class="genres-selector">
                <div class="genres-grid">
                  <button
                    type="button"
                    v-for="genre in availableGenres"
                    :key="genre"
                    class="genre-tag"
                    :class="{
                      selected: profileForm.genres.includes(genre),
                      'limit-reached':
                        profileForm.genres.length >= 5 && !profileForm.genres.includes(genre),
                    }"
                    @click="toggleGenre(genre)"
                    :disabled="
                      profileForm.genres.length >= 5 && !profileForm.genres.includes(genre)
                    "
                  >
                    {{ genre }}
                  </button>
                </div>
                <div class="selected-info">Выбрано: {{ profileForm.genres.length }} из 5</div>
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="profileLoading">
                {{ profileLoading ? 'Сохранение...' : 'Сохранить изменения' }}
              </button>
            </div>

            <div v-if="profileError" class="alert alert-error">
              {{ profileError }}
            </div>
            <div v-if="profileSuccess" class="alert alert-success">Профиль успешно обновлен!</div>
          </form>
        </div>

        <div v-if="activeTab === 'security'" class="tab-content">
          <h2>Безопасность</h2>
          <form @submit.prevent="changePassword" class="settings-form">
            <div class="form-group">
              <label for="currentPassword">Текущий пароль</label>
              <input
                id="currentPassword"
                v-model="passwordForm.currentPassword"
                type="password"
                class="form-control"
                required
              />
            </div>

            <div class="form-group">
              <label for="newPassword">Новый пароль</label>
              <input
                id="newPassword"
                v-model="passwordForm.newPassword"
                type="password"
                class="form-control"
                required
                minlength="6"
              />
              <small class="form-text">Минимум 6 символов</small>
            </div>

            <div class="form-group">
              <label for="confirmPassword">Подтвердите новый пароль</label>
              <input
                id="confirmPassword"
                v-model="passwordForm.confirmPassword"
                type="password"
                class="form-control"
                required
              />
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="passwordLoading">
                {{ passwordLoading ? 'Смена...' : 'Сменить пароль' }}
              </button>
            </div>

            <div v-if="passwordError" class="alert alert-error">
              {{ passwordError }}
            </div>
            <div v-if="passwordSuccess" class="alert alert-success">Пароль успешно изменен!</div>
          </form>
        </div>

        <div v-if="activeTab === 'account'" class="tab-content">
          <h2>Управление аккаунтом</h2>

          <div class="account-actions">
            <div class="account-action">
              <h3>Удаление аккаунта</h3>
              <p>Это действие нельзя отменить. Все ваши данные будут удалены.</p>
              <button class="btn btn-danger" @click="showDeleteModal = true">
                Удалить аккаунт
              </button>
            </div>

            <div class="account-action">
              <h3>Выход из аккаунта</h3>
              <p>Завершите текущую сессию на этом устройстве</p>
              <button class="btn btn-secondary" @click="logout">Выйти</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Удаление аккаунта</h2>
          <button class="close-btn" @click="showDeleteModal = false">✕</button>
        </div>

        <div class="modal-body">
          <p>
            Это действие нельзя отменить. Все ваши посты, плейлисты и другие данные будут удалены.
          </p>

          <form @submit.prevent="deleteAccount" class="delete-form">
            <div class="form-group">
              <label for="deletePassword">Введите пароль для подтверждения</label>
              <input
                id="deletePassword"
                v-model="deleteForm.password"
                type="password"
                class="form-control"
                required
              />
            </div>

            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">
                Отмена
              </button>
              <button type="submit" class="btn btn-danger" :disabled="deleteLoading">
                {{ deleteLoading ? 'Удаление...' : 'Удалить аккаунт' }}
              </button>
            </div>

            <div v-if="deleteError" class="alert alert-error">
              {{ deleteError }}
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'SettingsView',
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  data() {
    return {
      activeTab: 'profile',
      tabs: [
        { id: 'profile', label: 'Профиль' },
        { id: 'security', label: 'Безопасность' },
        { id: 'account', label: 'Аккаунт' },
      ],
      profileForm: {
        username: '',
        bio: '',
        location: '',
        genres: [],
      },
      availableGenres: [
        'Rock',
        'Pop',
        'Hip-Hop',
        'Jazz',
        'Classical',
        'Electronic',
        'Indie',
        'Metal',
        'Folk',
        'R&B',
        'Soul',
        'Reggae',
        'Country',
        'Blues',
        'Funk',
        'Alternative',
        'Punk',
        'Disco',
        'House',
        'Techno',
        'Trance',
        'Dubstep',
        'Reggaeton',
        'Salsa',
        'K-Pop',
        'J-Pop',
        'Lo-Fi',
        'Ambient',
        'Instrumental',
      ],
      profileLoading: false,
      profileError: null,
      profileSuccess: false,
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      },
      passwordLoading: false,
      passwordError: null,
      passwordSuccess: false,
      showDeleteModal: false,
      deleteForm: {
        password: '',
      },
      deleteLoading: false,
      deleteError: null,
    }
  },
  mounted() {
    this.loadUserData()
  },
  methods: {
    loadUserData() {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      this.profileForm = {
        username: user.username || '',
        bio: user.bio || '',
        location: user.location || '',
        genres: Array.isArray(user.genres) ? user.genres : user.genres ? [user.genres] : [],
      }
    },

    toggleGenre(genre) {
      const index = this.profileForm.genres.indexOf(genre)
      if (index === -1) {
        if (this.profileForm.genres.length < 5) {
          this.profileForm.genres.push(genre)
        }
      } else {
        this.profileForm.genres.splice(index, 1)
      }
    },

    async updateProfile() {
      if (this.profileForm.genres.length > 5) {
        this.profileError = 'Выберите не более 5 жанров'
        return
      }

      this.profileLoading = true
      this.profileError = null
      this.profileSuccess = false

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('/api/profile/update', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.profileForm),
        })

        const data = await response.json()

        if (data.success) {
          this.profileSuccess = true
          localStorage.setItem('user', JSON.stringify(data.user))
          this.authStore.user = data.user

          setTimeout(() => {
            this.profileSuccess = false
          }, 3000)
        } else {
          this.profileError = data.error || 'Ошибка при обновлении профиля'
        }
      } catch (err) {
        this.profileError = 'Ошибка сети. Попробуйте позже.'
        console.error('Update profile error:', err)
      } finally {
        this.profileLoading = false
      }
    },

    async changePassword() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.passwordError = 'Новые пароли не совпадают'
        return
      }

      if (this.passwordForm.newPassword.length < 6) {
        this.passwordError = 'Новый пароль должен содержать минимум 6 символов'
        return
      }

      this.passwordLoading = true
      this.passwordError = null
      this.passwordSuccess = false

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('/api/auth/change-password', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            current_password: this.passwordForm.currentPassword,
            new_password: this.passwordForm.newPassword,
          }),
        })

        const data = await response.json()

        if (data.success) {
          this.passwordSuccess = true
          this.passwordForm = {
            currentPassword: '',
            newPassword: '',
            confirmPassword: '',
          }

          setTimeout(() => {
            this.passwordSuccess = false
          }, 3000)
        } else {
          this.passwordError = data.error || 'Ошибка при смене пароля'
        }
      } catch (err) {
        this.passwordError = 'Ошибка сети. Попробуйте позже.'
        console.error('Change password error:', err)
      } finally {
        this.passwordLoading = false
      }
    },

    logout() {
      this.authStore.logout()
    },

    async deleteAccount() {
      if (!this.deleteForm.password) {
        this.deleteError = 'Введите пароль'
        return
      }

      this.deleteLoading = true
      this.deleteError = null

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('/api/auth/delete-account', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            password: this.deleteForm.password,
          }),
        })

        const data = await response.json()

        if (data.success) {
          this.authStore.logout()
          this.$router.push('/')
        } else {
          this.deleteError = data.error || 'Ошибка при удалении аккаунта'
        }
      } catch (err) {
        this.deleteError = 'Ошибка сети. Попробуйте позже.'
        console.error('Delete account error:', err)
      } finally {
        this.deleteLoading = false
      }
    },
  },
}
</script>

<style scoped>
.settings-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.settings-header {
  text-align: center;
  margin: 2rem 0 3rem;
}

.settings-header h1 {
  font-size: 2.5rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.settings-header p {
  color: #b0b0b0;
  font-size: 1.2rem;
}

.settings-container {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  overflow: hidden;
}

.settings-tabs {
  display: flex;
  background: rgba(255, 255, 255, 0.08);
  border-bottom: 1px solid #333;
}

.settings-tabs button {
  flex: 1;
  padding: 1.2rem;
  background: transparent;
  border: none;
  color: #b0b0b0;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s;
  position: relative;
}

.settings-tabs button:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.settings-tabs button.active {
  color: #8a2be2;
}

.settings-tabs button.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #8a2be2;
}

.settings-content {
  padding: 2rem;
}

.tab-content h2 {
  color: white;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.settings-form {
  max-width: 600px;
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

.form-control {
  width: 100%;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  font-family: inherit;
}

.form-control:focus {
  outline: none;
  border-color: #8a2be2;
  background: rgba(255, 255, 255, 0.12);
}

.form-text {
  display: block;
  margin-top: 0.5rem;
  color: #888;
  font-size: 0.9rem;
}

.form-hint {
  display: block;
  margin-bottom: 0.8rem;
  color: #888;
  font-size: 0.85rem;
}

.genres-selector {
  margin-top: 1rem;
}

.genres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.genre-tag {
  padding: 0.6rem 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 8px;
  color: #b0b0b0;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.genre-tag:hover:not(:disabled) {
  background: rgba(138, 43, 226, 0.1);
  border-color: #8a2be2;
  transform: translateY(-1px);
}

.genre-tag.selected {
  background: rgba(138, 43, 226, 0.2);
  border-color: #8a2be2;
  color: #8a2be2;
  font-weight: 500;
}

.genre-tag.limit-reached {
  opacity: 0.4;
  cursor: not-allowed;
}

.genre-tag:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.selected-info {
  color: #8a2be2;
  font-size: 0.9rem;
  text-align: right;
}

.form-actions {
  margin-top: 2rem;
}

.btn {
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
}

.btn-primary {
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: white;
  border: 1px solid #444;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.btn-danger {
  background: linear-gradient(90deg, #ff4757, #c23636);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 71, 87, 0.3);
}

.alert {
  padding: 1rem;
  border-radius: 10px;
  margin-top: 1rem;
  text-align: center;
}

.alert-error {
  background: rgba(255, 71, 87, 0.1);
  border: 1px solid #ff4757;
  color: #ff4757;
}

.alert-success {
  background: rgba(46, 213, 115, 0.1);
  border: 1px solid #2ed573;
  color: #2ed573;
}

.account-actions {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  max-width: 600px;
}

.account-action {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border: 1px solid #333;
}

.account-action h3 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.account-action p {
  color: #b0b0b0;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: #1e1e2e;
  border-radius: 15px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #333;
}

.modal-header h2 {
  color: white;
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: transparent;
  border: none;
  color: #888;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 5px;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.modal-body {
  padding: 1.5rem;
}

.modal-body p {
  color: #b0b0b0;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.delete-form {
  margin-top: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .settings-tabs {
    flex-direction: column;
  }

  .settings-tabs button {
    text-align: center;
    border-bottom: 1px solid #333;
  }

  .settings-tabs button.active::after {
    display: none;
  }

  .genres-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }

  .modal-actions {
    flex-direction: column;
  }

  .modal-actions .btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .genres-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .account-action {
    text-align: center;
  }
}
</style>
