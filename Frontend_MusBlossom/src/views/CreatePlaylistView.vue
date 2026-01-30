<template>
  <div class="create-playlist-view">
    <div class="create-header">
      <h1>Создать новый плейлист</h1>
      <p>Соберите свою коллекцию любимых треков</p>
    </div>

    <div class="create-container">
      <div class="playlist-form">
        <div class="form-section">
          <h2>Основная информация</h2>

          <div class="form-group">
            <label for="playlist-name">Название плейлиста</label>
            <input
              type="text"
              id="playlist-name"
              v-model="playlist.name"
              placeholder="Например: 'Лучшие треки 2024'"
            />
          </div>

          <div class="form-group">
            <label for="playlist-description">Описание</label>
            <textarea
              id="playlist-description"
              v-model="playlist.description"
              placeholder="Расскажите о вашем плейлисте..."
              rows="4"
            ></textarea>
          </div>

          <div class="form-group">
            <label>Обложка плейлиста</label>
            <div class="cover-upload">
              <div class="cover-preview" @click="triggerFileUpload">
                <img v-if="playlist.cover" :src="playlist.cover" alt="Cover" />
                <div v-else class="cover-placeholder">
                  <span>+</span>
                  <p>Загрузить обложку</p>
                </div>
                <input
                  type="file"
                  ref="fileInput"
                  @change="handleFileUpload"
                  accept="image/*"
                  hidden
                />
              </div>
              <div class="cover-options">
                <button type="button" @click="triggerFileUpload">Загрузить</button>
                <button type="button" @click="useDefaultCover">Использовать шаблон</button>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>Настройки приватности</label>
            <div class="privacy-options">
              <label class="radio-option">
                <input type="radio" v-model="playlist.isPublic" :value="true" />
                <span>Публичный</span>
                <small>Виден всем пользователям</small>
              </label>
              <label class="radio-option">
                <input type="radio" v-model="playlist.isPublic" :value="false" />
                <span>Приватный</span>
                <small>Только для вас</small>
              </label>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h2>Добавить треки</h2>

          <div class="search-tracks">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Поиск треков..."
              @input="searchTracks"
            />
          </div>

          <div v-if="searchResults.length" class="search-results">
            <div class="results-header">
              <span>Найденные треки</span>
              <span>{{ searchResults.length }} результатов</span>
            </div>
            <div class="tracks-list">
              <div v-for="track in searchResults" :key="track.id" class="track-item">
                <img :src="track.cover" :alt="track.title" class="track-cover" />
                <div class="track-info">
                  <span class="track-title">{{ track.title }}</span>
                  <span class="track-artist">{{ track.artist }}</span>
                  <span class="track-album">{{ track.album }}</span>
                </div>
                <span class="track-duration">{{ formatDuration(track.duration) }}</span>
                <button class="add-btn" @click="addTrack(track)" :disabled="isTrackAdded(track.id)">
                  {{ isTrackAdded(track.id) ? '✓' : '+' }}
                </button>
              </div>
            </div>
          </div>

          <div v-if="selectedTracks.length" class="selected-tracks">
            <h3>Добавленные треки ({{ selectedTracks.length }})</h3>
            <div class="selected-list">
              <div v-for="(track, index) in selectedTracks" :key="track.id" class="selected-item">
                <span class="track-number">{{ index + 1 }}</span>
                <img :src="track.cover" :alt="track.title" class="track-cover" />
                <div class="track-info">
                  <span class="track-title">{{ track.title }}</span>
                  <span class="track-artist">{{ track.artist }}</span>
                </div>
                <span class="track-duration">{{ formatDuration(track.duration) }}</span>
                <button class="remove-btn" @click="removeTrack(track.id)">×</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="playlist-preview">
        <div class="preview-card">
          <div class="preview-cover">
            <img v-if="playlist.cover" :src="playlist.cover" alt="Cover" />
            <div v-else class="preview-placeholder"></div>
          </div>
          <div class="preview-info">
            <h3>{{ playlist.name || 'Новый плейлист' }}</h3>
            <p class="preview-description">{{ playlist.description || 'Описание отсутствует' }}</p>
            <div class="preview-meta">
              <span class="meta-item">{{ selectedTracks.length }} треков</span>
              <span class="meta-item">{{ playlist.isPublic ? 'Публичный' : 'Приватный' }}</span>
            </div>
          </div>
        </div>

        <div class="preview-actions">
          <button class="btn btn-secondary" @click="resetForm">Сбросить</button>
          <button
            class="btn btn-primary"
            @click="createPlaylist"
            :disabled="!playlist.name || selectedTracks.length === 0"
          >
            Создать плейлист
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CreatePlaylistView',
  data() {
    return {
      playlist: {
        name: '',
        description: '',
        cover: '',
        isPublic: true,
      },
      searchQuery: '',
      searchResults: [],
      selectedTracks: [],
      defaultCovers: [
        'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=400&fit=crop',
        'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=800&h=400&fit=crop',
        'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=800&h=400&fit=crop',
      ],
    }
  },
  methods: {
    triggerFileUpload() {
      this.$refs.fileInput.click()
    },

    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.playlist.cover = e.target.result
        }
        reader.readAsDataURL(file)
      }
    },

    useDefaultCover() {
      const randomIndex = Math.floor(Math.random() * this.defaultCovers.length)
      this.playlist.cover = this.defaultCovers[randomIndex]
    },

    searchTracks() {
      if (this.searchQuery.length < 2) {
        this.searchResults = []
        return
      }

      this.searchResults = [
        {
          id: 1,
          title: 'Blinding Lights',
          artist: 'The Weeknd',
          album: 'After Hours',
          cover:
            'https://i.scdn.co/image/ab67616d00001e02/86a0f12c8d1c65b6e6c8b1a0f2c5e8b1d5b3a8f2',
          duration: 200000,
        },
        {
          id: 2,
          title: 'Levitating',
          artist: 'Dua Lipa',
          album: 'Future Nostalgia',
          cover:
            'https://i.scdn.co/image/ab67616d00001e02/f2b8b5b5f5b5f5b5f5b5f5b5f5b5f5b5f5b5f5b5',
          duration: 203000,
        },
      ]
    },

    addTrack(track) {
      if (!this.isTrackAdded(track.id)) {
        this.selectedTracks.push(track)
      }
    },

    removeTrack(trackId) {
      this.selectedTracks = this.selectedTracks.filter((t) => t.id !== trackId)
    },

    isTrackAdded(trackId) {
      return this.selectedTracks.some((t) => t.id === trackId)
    },

    formatDuration(ms) {
      const minutes = Math.floor(ms / 60000)
      const seconds = ((ms % 60000) / 1000).toFixed(0)
      return `${minutes}:${seconds.padStart(2, '0')}`
    },

    resetForm() {
      this.playlist = {
        name: '',
        description: '',
        cover: '',
        isPublic: true,
      }
      this.selectedTracks = []
      this.searchResults = []
      this.searchQuery = ''
    },

    async createPlaylist() {
      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('http://localhost:5000/api/playlists', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            name: this.playlist.name,
            description: this.playlist.description,
            is_public: this.playlist.isPublic,
          }),
        })

        const data = await response.json()
        if (data.success) {
          alert('Плейлист успешно создан!')
          this.$router.push(`/playlists/${data.playlist.id}`)
        } else {
          alert('Ошибка: ' + data.error)
        }
      } catch (error) {
        console.error('Error creating playlist:', error)
        alert('Ошибка создания плейлиста')
      }
    },
  },
}
</script>

<style scoped>
.create-playlist-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.create-header {
  text-align: center;
  margin: 2rem 0 3rem;
}

.create-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: white;
}

.create-header p {
  color: #b0b0b0;
  font-size: 1.2rem;
}

.create-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
}

.playlist-form {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.form-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
}

.form-section h2 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #333;
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

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #8a2be2;
}

.cover-upload {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.cover-preview {
  width: 200px;
  height: 200px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  border: 2px dashed #444;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  text-align: center;
  color: #888;
}

.cover-placeholder span {
  font-size: 3rem;
  display: block;
  margin-bottom: 0.5rem;
}

.cover-options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.cover-options button {
  padding: 0.8rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  font-size: 1rem;
}

.cover-options button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.privacy-options {
  display: flex;
  gap: 2rem;
}

.radio-option {
  flex: 1;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  cursor: pointer;
  border: 1px solid #444;
  transition: all 0.3s;
}

.radio-option:hover {
  background: rgba(255, 255, 255, 0.08);
}

.radio-option input {
  margin-right: 0.5rem;
}

.radio-option span {
  display: block;
  color: white;
  font-weight: 500;
  margin-bottom: 0.3rem;
}

.radio-option small {
  color: #888;
  font-size: 0.9rem;
}

.search-tracks input {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.search-results {
  margin-bottom: 2rem;
}

.results-header {
  display: flex;
  justify-content: space-between;
  color: #888;
  margin-bottom: 1rem;
  padding: 0 0.5rem;
}

.tracks-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 400px;
  overflow-y: auto;
}

.track-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  transition: background 0.3s;
}

.track-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.track-cover {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  object-fit: cover;
}

.track-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.track-title {
  color: white;
  font-weight: 500;
  margin-bottom: 0.2rem;
}

.track-artist {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.2rem;
}

.track-album {
  color: #888;
  font-size: 0.85rem;
}

.track-duration {
  color: #888;
  font-size: 0.9rem;
}

.add-btn {
  width: 40px;
  height: 40px;
  background: #8a2be2;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: bold;
}

.add-btn:disabled {
  background: #2ed573;
  cursor: not-allowed;
}

.selected-tracks h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.selected-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.selected-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.track-number {
  color: #8a2be2;
  font-weight: bold;
  min-width: 30px;
}

.remove-btn {
  width: 30px;
  height: 30px;
  background: rgba(255, 71, 87, 0.1);
  color: #ff4757;
  border: 1px solid rgba(255, 71, 87, 0.3);
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
}

.playlist-preview {
  position: sticky;
  top: 100px;
  height: fit-content;
}

.preview-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.preview-cover {
  height: 200px;
  background: rgba(255, 255, 255, 0.03);
}

.preview-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #8a2be2, #4b0082);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
}

.preview-info {
  padding: 1.5rem;
}

.preview-info h3 {
  color: white;
  margin-bottom: 0.8rem;
  font-size: 1.3rem;
}

.preview-description {
  color: #b0b0b0;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.preview-meta {
  display: flex;
  gap: 1rem;
  color: #888;
  font-size: 0.9rem;
}

.preview-actions {
  display: flex;
  gap: 1rem;
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

@media (max-width: 1024px) {
  .create-container {
    grid-template-columns: 1fr;
  }

  .playlist-preview {
    position: static;
  }
}

@media (max-width: 768px) {
  .cover-upload {
    flex-direction: column;
  }

  .privacy-options {
    flex-direction: column;
    gap: 1rem;
  }

  .preview-actions {
    flex-direction: column;
  }
}
</style>
