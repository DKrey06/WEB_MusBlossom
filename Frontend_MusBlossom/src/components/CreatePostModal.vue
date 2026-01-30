<template>
  <div class="create-post-modal">
    <div class="modal-overlay" @click="close">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Создать пост</h2>
          <button class="close-btn" @click="close">✕</button>
        </div>

        <form @submit.prevent="submitPost" class="create-post-form">
          <div class="form-group">
            <label for="postTitle">Заголовок *</label>
            <input
              id="postTitle"
              v-model="form.title"
              placeholder="О чем хочешь рассказать?"
              required
            />
          </div>

          <div class="form-group">
            <label for="postType">Тип поста</label>
            <select id="postType" v-model="form.post_type">
              <option value="thought">Мысли</option>
              <option value="review">Рецензия</option>
              <option value="news">Новости</option>
              <option value="quote">Цитата</option>
            </select>
          </div>

          <div class="form-group">
            <label for="postContent">Содержание *</label>
            <textarea
              id="postContent"
              v-model="form.content"
              placeholder="Поделись своими мыслями..."
              rows="6"
              required
            ></textarea>
            <div class="char-counter">{{ form.content.length }}/5000</div>
          </div>

          <div class="form-group">
            <label>Прикрепить трек</label>
            <div class="track-attachment">
              <input v-model="form.track_name" placeholder="Название трека" class="track-input" />
              <input v-model="form.artist_name" placeholder="Исполнитель" class="track-input" />
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="close">Отмена</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Публикация...' : 'Опубликовать' }}
            </button>
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'CreatePostModal',
  props: {
    postToEdit: {
      type: Object,
      default: null,
    },
  },
  emits: ['close', 'created'],
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  data() {
    return {
      form: {
        title: '',
        content: '',
        post_type: 'thought',
        track_name: '',
        artist_name: '',
      },
      loading: false,
      error: null,
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },

    async submitPost() {
      if (!this.form.title.trim() || !this.form.content.trim()) {
        this.error = 'Заполните все обязательные поля'
        return
      }

      this.loading = true
      this.error = null

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('/api/posts', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.form),
        })

        const data = await response.json()

        if (data.success) {
          this.$emit('created', data.post)
          this.resetForm()
        } else {
          this.error = data.error || 'Ошибка при создании поста'
        }
      } catch (err) {
        this.error = 'Ошибка сети. Попробуйте позже.'
        console.error('Create post error:', err)
      } finally {
        this.loading = false
      }
    },

    resetForm() {
      this.form = {
        title: '',
        content: '',
        post_type: 'thought',
        track_name: '',
        artist_name: '',
      }
    },
  },
}
</script>

<style scoped>
.create-post-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
}

.modal-overlay {
  background: rgba(0, 0, 0, 0.7);
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
  max-width: 600px;
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

.create-post-form {
  padding: 1.5rem;
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

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #8a2be2;
  background: rgba(255, 255, 255, 0.12);
}

.track-attachment {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.char-counter {
  text-align: right;
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.3rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  flex: 1;
  padding: 1rem;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
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
}
</style>
