<template>
  <div class="create-post-view">
    <div class="create-header">
      <h1>Создать пост</h1>
      <p>Поделись своими мыслями или музыкой</p>
    </div>

    <div class="create-container">
      <form @submit.prevent="createPost" class="post-form">
        <div class="form-group">
          <label for="post-title">Заголовок *</label>
          <input
            type="text"
            id="post-title"
            v-model="post.title"
            placeholder="О чем хочешь рассказать?"
            required
          />
        </div>

        <div class="form-group">
          <label for="post-content">Содержание *</label>
          <textarea
            id="post-content"
            v-model="post.content"
            placeholder="Напиши свой пост здесь..."
            rows="8"
            required
          ></textarea>
          <div class="char-counter">{{ post.content.length }}/5000</div>
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
          <label>Привязать трек</label>
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
              placeholder="Добавьте теги (нажмите Enter)..."
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

        <div class="form-group">
          <label>Прикрепить изображение</label>
          <div class="image-upload">
            <input
              type="file"
              ref="fileInput"
              accept="image/*"
              @change="handleImageUpload"
              style="display: none"
            />
            <div v-if="!post.image" class="upload-placeholder" @click="triggerFileInput">
              <span class="upload-icon">📷</span>
              <span>Загрузить фото</span>
              <small>До 5 MB, форматы: JPG, PNG</small>
            </div>
            <div v-else class="image-preview">
              <img :src="post.image" alt="Preview" />
              <button type="button" class="remove-image" @click="removeImage">×</button>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="cancelCreate">Отмена</button>
          <button type="submit" class="btn btn-primary" :disabled="creating">
            {{ creating ? 'Создание...' : 'Опубликовать' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CreatePostView',
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
        image: null,
      },
      creating: false,
      postTypes: [
        { value: 'thought', label: 'Мысли' },
        { value: 'review', label: 'Рецензия' },
        { value: 'news', label: 'Новости' },
        { value: 'quote', label: 'Цитата' },
        { value: 'photo', label: 'Фото' },
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
        'Новинка',
        'Концерт',
        'Альбом',
        'Исполнитель',
      ],
    }
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
    async createPost() {
      this.creating = true

      try {
        const token = localStorage.getItem('access_token')
        const formData = new FormData()

        formData.append('title', this.post.title)
        formData.append('content', this.post.content)
        formData.append('post_type', this.post.post_type)
        formData.append('track_name', this.post.track_name)
        formData.append('artist_name', this.post.artist_name)
        formData.append('tags', JSON.stringify(this.post.tags))

        if (this.$refs.fileInput.files[0]) {
          formData.append('image', this.$refs.fileInput.files[0])
        }

        const response = await fetch('http://localhost:5000/api/posts', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        })

        const data = await response.json()
        if (data.success) {
          this.$router.push('/posts')
        } else {
          alert('Ошибка: ' + data.error)
        }
      } catch (error) {
        console.error('Error creating post:', error)
        alert('Ошибка создания поста')
      } finally {
        this.creating = false
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
        {
          id: 3,
          title: 'Stay',
          artist: 'The Kid LAROI, Justin Bieber',
          cover: 'https://i.scdn.co/image/ab67616d00001e02/6e0b5b8b9c5b8b8b8b8b8b8b8b8b8b8b8b8b8b8',
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

    triggerFileInput() {
      this.$refs.fileInput.click()
    },

    handleImageUpload(event) {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 5 * 1024 * 1024) {
          alert('Файл слишком большой (максимум 5 MB)')
          return
        }

        const reader = new FileReader()
        reader.onload = (e) => {
          this.post.image = e.target.result
        }
        reader.readAsDataURL(file)
      }
    },

    removeImage() {
      this.post.image = null
      this.$refs.fileInput.value = null
    },

    cancelCreate() {
      if (this.post.title || this.post.content) {
        if (confirm('Отменить создание поста? Все несохраненные изменения будут потеряны.')) {
          this.$router.go(-1)
        }
      } else {
        this.$router.go(-1)
      }
    },
  },
}
</script>

<style scoped>
.create-post-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.create-header {
  margin: 2rem 0 3rem;
}

.create-header h1 {
  font-size: 2.5rem;
  color: white;
  margin-bottom: 0.5rem;
}

.create-header p {
  color: #b0b0b0;
  font-size: 1.1rem;
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

.char-counter {
  text-align: right;
  color: #888;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.type-options {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.type-option {
  padding: 0.8rem 1.5rem;
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

.image-upload {
  cursor: pointer;
}

.upload-placeholder {
  padding: 2rem;
  background: rgba(255, 255, 255, 0.03);
  border: 2px dashed #444;
  border-radius: 10px;
  text-align: center;
  transition: all 0.3s;
}

.upload-placeholder:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: #8a2be2;
}

.upload-icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 1rem;
}

.upload-placeholder span {
  color: white;
  display: block;
  margin-bottom: 0.5rem;
}

.upload-placeholder small {
  color: #888;
  font-size: 0.9rem;
}

.image-preview {
  position: relative;
  width: 100%;
  max-width: 300px;
}

.image-preview img {
  width: 100%;
  border-radius: 10px;
}

.remove-image {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 30px;
  height: 30px;
  background: rgba(255, 71, 87, 0.9);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
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
