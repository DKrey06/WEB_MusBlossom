<template>
  <div class="edit-profile-modal">
    <div class="modal-overlay" @click="close">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Редактировать профиль</h2>
          <button class="close-btn" @click="close">✕</button>
        </div>

        <form @submit.prevent="updateProfile" class="edit-form">
          <div class="form-section">
            <h3>Основная информация</h3>

            <div class="form-group">
              <label for="username">Имя пользователя</label>
              <input
                id="username"
                v-model="form.username"
                placeholder="musiclover"
                required
                disabled
              />
              <small class="form-hint">Имя пользователя нельзя изменить</small>
            </div>

            <div class="form-group">
              <label for="bio">О себе</label>
              <textarea
                id="bio"
                v-model="form.bio"
                placeholder="Расскажите о своих музыкальных предпочтениях..."
                rows="3"
                maxlength="500"
              ></textarea>
              <div class="char-counter">{{ form.bio.length }}/500</div>
            </div>
          </div>

          <div class="form-section">
            <h3>Музыкальные предпочтения</h3>
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
                      selected: form.genres.includes(genre),
                      'limit-reached': form.genres.length >= 5 && !form.genres.includes(genre),
                    }"
                    @click="toggleGenre(genre)"
                    :disabled="form.genres.length >= 5 && !form.genres.includes(genre)"
                  >
                    {{ genre }}
                  </button>
                </div>
                <div class="selected-genres">
                  <div v-if="form.genres.length > 0" class="selected-list">
                    <span>Выбрано: {{ form.genres.join(', ') }}</span>
                  </div>
                  <div v-else class="no-selection">
                    <span>Жанры не выбраны</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3>Настройки приватности</h3>

            <div class="privacy-setting">
              <div class="setting-info">
                <h4>Профиль</h4>
                <p>Кто может просматривать ваш профиль</p>
              </div>
              <select v-model="form.privacy.profile" class="privacy-select">
                <option value="public">Все</option>
                <option value="friends">Только друзья</option>
                <option value="private">Только я</option>
              </select>
            </div>

            <div class="privacy-setting">
              <div class="setting-info">
                <h4>Посты</h4>
                <p>Кто может видеть ваши посты</p>
              </div>
              <select v-model="form.privacy.posts" class="privacy-select">
                <option value="public">Все</option>
                <option value="friends">Только друзья</option>
                <option value="private">Только я</option>
              </select>
            </div>

            <div class="privacy-setting">
              <div class="setting-info">
                <h4>Плейлисты</h4>
                <p>Кто может видеть ваши плейлисты</p>
              </div>
              <select v-model="form.privacy.playlists" class="privacy-select">
                <option value="public">Все</option>
                <option value="friends">Только друзья</option>
                <option value="private">Только я</option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="close">Отмена</button>
            <button type="submit" class="btn btn-primary" :disabled="loading || !isFormValid">
              {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
            </button>
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>
          <div v-if="success" class="success-message">Профиль успешно обновлен!</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditProfileModal',
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  emits: ['close', 'updated'],
  data() {
    return {
      form: {
        username: '',
        bio: '',
        genres: [],
        privacy: {
          profile: 'public',
          posts: 'public',
          playlists: 'public',
        },
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
      loading: false,
      error: null,
      success: false,
    }
  },
  computed: {
    isFormValid() {
      return this.form.bio.length <= 500
    },
  },
  mounted() {
    this.initializeForm()
  },
  methods: {
    initializeForm() {
      this.form = {
        username: this.user.username || '',
        bio: this.user.bio || '',
        genres: Array.isArray(this.user.genres)
          ? this.user.genres
          : this.user.genres
            ? [this.user.genres]
            : [],
        privacy: this.user.privacy || {
          profile: 'public',
          posts: 'public',
          playlists: 'public',
        },
      }
    },

    close() {
      this.$emit('close')
    },

    toggleGenre(genre) {
      const index = this.form.genres.indexOf(genre)
      if (index === -1) {
        if (this.form.genres.length < 5) {
          this.form.genres.push(genre)
        }
      } else {
        this.form.genres.splice(index, 1)
      }
    },

    async updateProfile() {
      if (!this.isFormValid) {
        this.error = 'Описание слишком длинное'
        return
      }

      if (this.form.genres.length > 5) {
        this.error = 'Выберите не более 5 жанров'
        return
      }

      this.loading = true
      this.error = null
      this.success = false

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('/api/profile/update', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.form),
        })

        const data = await response.json()

        if (data.success) {
          this.success = true
          const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
          const updatedUser = { ...storedUser, ...data.user }
          localStorage.setItem('user', JSON.stringify(updatedUser))
          setTimeout(() => {
            this.$emit('updated', data.user)
            this.close()
          }, 1500)
        } else {
          this.error = data.error || 'Ошибка при обновлении профиля'
        }
      } catch (err) {
        this.error = 'Ошибка сети. Попробуйте позже.'
        console.error('Update profile error:', err)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.edit-profile-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
}

.modal-overlay {
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 1rem;
}

.modal-content {
  background: #1e1e2e;
  border-radius: 15px;
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #333;
  position: sticky;
  top: 0;
  background: #1e1e2e;
  z-index: 1;
}

.modal-header h2 {
  color: white;
  margin: 0;
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

.edit-form {
  padding: 1.5rem;
}

.form-section {
  margin-bottom: 2.5rem;
}

.form-section h3 {
  color: white;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #333;
  font-size: 1.3rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: white;
  font-weight: 500;
  font-size: 0.95rem;
}

.form-hint {
  display: block;
  margin-bottom: 0.8rem;
  color: #888;
  font-size: 0.85rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  font-family: inherit;
}

.form-group input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #8a2be2;
  background: rgba(255, 255, 255, 0.12);
}

.char-counter {
  text-align: right;
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.3rem;
}

.genres-selector {
  margin-top: 1rem;
}

.genres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
  margin-bottom: 1.5rem;
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

.selected-genres {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px dashed #444;
}

.selected-list {
  color: #8a2be2;
  font-weight: 500;
}

.no-selection {
  color: #666;
  font-style: italic;
}

.privacy-setting {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  margin-bottom: 1rem;
}

.setting-info h4 {
  color: white;
  margin-bottom: 0.2rem;
  font-size: 1rem;
}

.setting-info p {
  color: #888;
  font-size: 0.9rem;
}

.privacy-select {
  width: auto;
  min-width: 150px;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 5px;
  color: white;
}

.privacy-select:focus {
  border-color: #8a2be2;
  outline: none;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #333;
}

.btn {
  flex: 1;
  padding: 1rem;
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

.error-message {
  background: rgba(255, 71, 87, 0.1);
  border: 1px solid #ff4757;
  color: #ff4757;
  padding: 1rem;
  border-radius: 10px;
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

.success-message {
  background: rgba(46, 213, 115, 0.1);
  border: 1px solid #2ed573;
  color: #2ed573;
  padding: 1rem;
  border-radius: 10px;
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .modal-content {
    max-height: 95vh;
  }

  .genres-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }

  .privacy-setting {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .privacy-select {
    width: 100%;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .genres-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
