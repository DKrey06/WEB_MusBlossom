<template>
  <div class="edit-post-view">
    <div class="edit-header">
      <h1>Редактировать пост</h1>
    </div>

    <div class="edit-container">
      <form @submit.prevent="updatePost" class="post-form">
        <div class="form-group">
          <label for="post-title">Заголовок</label>
          <input
            type="text"
            id="post-title"
            v-model="post.title"
            placeholder="Введите заголовок..."
            required
          />
        </div>

        <div class="form-group">
          <label for="post-content">Содержание</label>
          <textarea
            id="post-content"
            v-model="post.content"
            placeholder="Напишите ваш пост..."
            rows="10"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label>Тип поста</label>
          <div class="type-options">
            <label v-for="type in postTypes" :key="type.value" class="type-option">
              <input type="radio" v-model="post.post_type" :value="type.value" />
              <span>{{ type.label }}</span>
            </label>
          </div>
        </div>

        <div v-if="post.post_type === 'review'" class="form-group">
          <label>Музыкальный трек</label>
          <div class="track-search">
            <input
              type="text"
              v-model="trackSearch"
              placeholder="Поиск трека..."
              @input="searchTracks"
            />
            <div v-if="trackResults.length" class="track-results">
              <div
                v-for="track in trackResults"
                :key="track.id"
                class="track-result"
                @click="selectTrack(track)"
              >
                <img :src="track.cover" :alt="track.title" class="track-cover" />
                <div class="track-info">
                  <span class="track-title">{{ track.title }}</span>
                  <span class="track-artist">{{ track.artist }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="post.track_name" class="selected-track">
            <div class="track-display">
              <img
                :src="post.track_cover || 'https://via.placeholder.com/50'"
                alt="Cover"
                class="track-cover"
              />
              <div class="track-details">
                <strong>{{ post.track_name }}</strong>
                <span v-if="post.artist_name">{{ post.artist_name }}</span>
              </div>
              <button type="button" class="remove-track" @click="removeTrack">×</button>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>Теги</label>
          <div class="tags-input">
            <div class="selected-tags">
              <span v-for="tag in post.tags" :key="tag" class="tag">
                {{ tag }}
                <button type="button" @click="removeTag(tag)" class="remove-tag">×</button>
              </span>
            </div>
            <input
              type="text"
              v-model="tagInput"
              placeholder="Добавьте теги..."
              @keydown.enter.prevent="addTag"
            />
            <div v-if="tagSuggestions.length" class="tag-suggestions">
              <div
                v-for="suggestion in tagSuggestions"
                :key="suggestion"
                class="suggestion"
                @click="addTagFromSuggestion(suggestion)"
              >
                {{ suggestion }}
              </div>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="cancelEdit">Отмена</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Сохранение...' : 'Сохранить изменения' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditPostView',
  data() {
    return {
      post: {
        title: '',
        content: '',
        post_type: 'thought',
        track_name: '',
        artist_name: '',
        track_cover: '',
        tags: [],
      },
      saving: false,
      postTypes: [
        { value: 'thought', label: 'Мысли' },
        { value: 'review', label: 'Рецензия' },
        { value: 'news', label: 'Новости' },
        { value: 'quote', label: 'Цитата' },
      ],
      trackSearch: '',
      trackResults: [],
      tagInput: '',
      tagSuggestions: [],
      allTags: [
        'Рок',
        'Поп',
        'Хип-хоп',
        'Джаз',
        'Классика',
        'Электроника',
        'Инди',
        'Метал',
        'Фолк',
        'R&B',
        'Соул',
        'Регги',
      ],
    }
  },
  async mounted() {
    await this.loadPost()
  },
  watch: {
    tagInput(newValue) {
      if (newValue.trim()) {
        this.tagSuggestions = this.allTags.filter(
          (tag) =>
            tag.toLowerCase().includes(newValue.toLowerCase()) && !this.post.tags.includes(tag),
        )
      } else {
        this.tagSuggestions = []
      }
    },
  },
  methods: {
    async loadPost() {
      try {
        const postId = this.$route.params.id
        const response = await fetch(`http://localhost:5000/api/posts/${postId}`)
        const data = await response.json()

        if (data.success) {
          this.post = {
            title: data.post.title,
            content: data.post.content,
            post_type: data.post.post_type,
            track_name: data.post.track_name,
            artist_name: data.post.artist_name,
            track_cover: data.post.album_art_url,
            tags: data.post.tags || [],
          }
        }
      } catch (error) {
        console.error('Error loading post:', error)
      }
    },

    searchTracks() {
      if (this.trackSearch.length < 2) {
        this.trackResults = []
        return
      }

      this.trackResults = [
        {
          id: 1,
          title: 'Blinding Lights',
          artist: 'The Weeknd',
          cover:
            'https://i.scdn.co/image/ab67616d00001e02/86a0f12c8d1c65b6e6c8b1a0f2c5e8b1d5b3a8f2',
        },
        {
          id: 2,
          title: 'Levitating',
          artist: 'Dua Lipa',
          cover:
            'https://i.scdn.co/image/ab67616d00001e02/f2b8b5b5f5b5f5b5f5b5f5b5f5b5f5b5f5b5f5b5',
        },
      ]
    },

    selectTrack(track) {
      this.post.track_name = track.title
      this.post.artist_name = track.artist
      this.post.track_cover = track.cover
      this.trackSearch = ''
      this.trackResults = []
    },

    removeTrack() {
      this.post.track_name = ''
      this.post.artist_name = ''
      this.post.track_cover = ''
    },

    addTag() {
      const tag = this.tagInput.trim()
      if (tag && !this.post.tags.includes(tag)) {
        this.post.tags.push(tag)
        this.tagInput = ''
        this.tagSuggestions = []
      }
    },

    addTagFromSuggestion(tag) {
      if (!this.post.tags.includes(tag)) {
        this.post.tags.push(tag)
        this.tagInput = ''
        this.tagSuggestions = []
      }
    },

    removeTag(tag) {
      this.post.tags = this.post.tags.filter((t) => t !== tag)
    },

    async updatePost() {
      this.saving = true

      try {
        const token = localStorage.getItem('access_token')
        const postId = this.$route.params.id

        const response = await fetch(`http://localhost:5000/api/posts/${postId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.post),
        })

        const data = await response.json()
        if (data.success) {
          this.$router.push(`/posts/${postId}`)
        } else {
          alert('Ошибка: ' + data.error)
        }
      } catch (error) {
        console.error('Error updating post:', error)
        alert('Ошибка сохранения поста')
      } finally {
        this.saving = false
      }
    },

    cancelEdit() {
      if (confirm('Отменить редактирование? Все несохраненные изменения будут потеряны.')) {
        this.$router.go(-1)
      }
    },
  },
}
</script>

<style scoped>
.edit-post-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.edit-header {
  margin: 2rem 0 3rem;
}

.edit-header h1 {
  font-size: 2rem;
  color: white;
}

.post-form {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
}

.form-group {
  margin-bottom: 2rem;
}

.form-group label {
  display: block;
  color: white;
  margin-bottom: 0.8rem;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  font-family: inherit;
}

.form-group textarea {
  resize: vertical;
  min-height: 200px;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #8a2be2;
}

.type-options {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.type-option {
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid #444;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.type-option:hover {
  background: rgba(255, 255, 255, 0.08);
}

.type-option input {
  margin-right: 0.5rem;
}

.type-option span {
  color: #b0b0b0;
}

.track-search {
  position: relative;
}

.track-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #1a1a2e;
  border: 1px solid #333;
  border-radius: 10px;
  margin-top: 0.5rem;
  max-height: 300px;
  overflow-y: auto;
  z-index: 10;
}

.track-result {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.track-result:hover {
  background: rgba(255, 255, 255, 0.05);
}

.track-cover {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  object-fit: cover;
}

.track-info {
  flex: 1;
}

.track-title {
  display: block;
  color: white;
  margin-bottom: 0.2rem;
}

.track-artist {
  color: #888;
  font-size: 0.9rem;
}

.selected-track {
  margin-top: 1rem;
}

.track-display {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.track-details {
  flex: 1;
}

.track-details strong {
  display: block;
  color: white;
  margin-bottom: 0.2rem;
}

.track-details span {
  color: #888;
  font-size: 0.9rem;
}

.remove-track {
  width: 30px;
  height: 30px;
  background: rgba(255, 71, 87, 0.1);
  color: #ff4757;
  border: 1px solid rgba(255, 71, 87, 0.3);
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
}

.tags-input {
  position: relative;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-radius: 20px;
  font-size: 0.9rem;
}

.remove-tag {
  background: none;
  border: none;
  color: #8a2be2;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tag-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #1a1a2e;
  border: 1px solid #333;
  border-radius: 10px;
  margin-top: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.suggestion {
  padding: 0.8rem 1rem;
  cursor: pointer;
  transition: background 0.3s;
  color: #b0b0b0;
}

.suggestion:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.form-actions {
  display: flex;
  gap: 1rem;
  padding-top: 2rem;
  border-top: 1px solid #333;
}

.btn {
  padding: 1rem 2rem;
  border-radius: 10px;
  border: none;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  flex: 1;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: white;
  border: 1px solid #444;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
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
</style>
