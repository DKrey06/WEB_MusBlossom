<template>
  <div class="playlist-detail-view">
    <div class="playlist-header">
      <div class="playlist-cover">
        <img :src="playlist.cover" alt="Playlist Cover" />
        <div class="playlist-actions">
          <button class="play-btn" @click="playPlaylist">▶️ Воспроизвести все</button>
          <button class="action-btn" @click="shufflePlaylist">🔀 Перемешать</button>
          <button class="action-btn" @click="savePlaylist">
            {{ isSaved ? '💾 Сохранено' : '💾 Сохранить' }}
          </button>
          <button class="action-btn" @click="sharePlaylist">↪️ Поделиться</button>
        </div>
      </div>
      <div class="playlist-info">
        <div class="playlist-meta">
          <span class="meta-item">🎵 Плейлист</span>
          <span class="meta-item">👤 {{ playlist.creator }}</span>
          <span class="meta-item">📅 {{ playlist.createdAt }}</span>
        </div>
        <h1 class="playlist-title">{{ playlist.title }}</h1>
        <p class="playlist-description">{{ playlist.description }}</p>
        <div class="playlist-stats">
          <span class="stat">{{ playlist.tracks.length }} треков</span>
          <span class="stat">{{ formatDuration(playlist.duration) }}</span>
          <span class="stat">{{ playlist.likes }} ❤️</span>
          <span class="stat">{{ playlist.plays }} 👁️</span>
        </div>
        <div class="playlist-tags">
          <span class="tag" v-for="tag in playlist.tags" :key="tag">{{ tag }}</span>
        </div>
      </div>
    </div>

    <div class="playlist-content">
      <div class="playlist-controls">
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск в плейлисте..."
            @input="searchTracks"
          />
          <span class="search-icon">🔍</span>
        </div>
        <div class="filter-buttons">
          <button @click="sortBy('title')" :class="{ active: sortBy === 'title' }">
            По названию
          </button>
          <button @click="sortBy('artist')" :class="{ active: sortBy === 'artist' }">
            По исполнителю
          </button>
          <button @click="sortBy('duration')" :class="{ active: sortBy === 'duration' }">
            По длительности
          </button>
          <button @click="sortBy('added')" :class="{ active: sortBy === 'added' }">
            По дате добавления
          </button>
        </div>
      </div>

      <div class="tracks-list">
        <div class="tracks-header">
          <div class="header-item">#</div>
          <div class="header-item">Название</div>
          <div class="header-item">Исполнитель</div>
          <div class="header-item">Альбом</div>
          <div class="header-item">Добавлено</div>
          <div class="header-item">⏱️</div>
          <div class="header-item">Действия</div>
        </div>

        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Загрузка треков...</p>
        </div>

        <div v-else class="tracks-container">
          <div
            v-for="(track, index) in filteredTracks"
            :key="track.id"
            class="track-item"
            :class="{ playing: isPlaying && currentTrack?.id === track.id }"
            @dblclick="playTrack(track)"
          >
            <div class="track-number">
              <span v-if="isPlaying && currentTrack?.id === track.id" class="playing-icon">▶️</span>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <div class="track-info">
              <img :src="track.cover" class="track-cover" alt="Cover" />
              <div class="track-details">
                <h4 class="track-title">{{ track.title }}</h4>
                <p class="track-artist">{{ track.artist }}</p>
              </div>
            </div>
            <div class="track-artist-info">{{ track.artist }}</div>
            <div class="track-album">{{ track.album }}</div>
            <div class="track-added">{{ track.added }}</div>
            <div class="track-duration">{{ formatTime(track.duration) }}</div>
            <div class="track-actions">
              <button class="action-btn" @click="playTrack(track)">▶️</button>
              <button class="action-btn" @click="toggleLikeTrack(track)">
                {{ track.isLiked ? '❤️' : '🤍' }}
              </button>
              <button class="action-btn" @click="addToQueue(track)">➕</button>
              <button v-if="isOwner" class="action-btn" @click="removeFromPlaylist(track.id)">
                🗑️
              </button>
            </div>
          </div>
        </div>

        <div v-if="filteredTracks.length === 0" class="no-tracks">
          <div class="no-tracks-icon">🎵</div>
          <h3>Треки не найдены</h3>
          <p>Попробуйте изменить параметры поиска</p>
        </div>
      </div>

      <div class="similar-playlists" v-if="similarPlaylists.length > 0">
        <h3>🎵 Похожие плейлисты</h3>
        <div class="playlists-grid">
          <div
            v-for="similar in similarPlaylists"
            :key="similar.id"
            class="playlist-card"
            @click="viewPlaylist(similar)"
          >
            <img :src="similar.cover" class="playlist-img" alt="Cover" />
            <div class="playlist-card-info">
              <h4>{{ similar.title }}</h4>
              <p>{{ similar.creator }}</p>
              <div class="playlist-card-stats">
                <span>{{ similar.tracks }} треков</span>
                <span>{{ similar.likes }} ❤️</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="comments-section">
        <div class="comments-header">
          <h3>💬 Обсуждение ({{ comments.length }})</h3>
          <button class="btn btn-small" @click="showCommentForm = !showCommentForm">
            Добавить комментарий
          </button>
        </div>

        <div v-if="showCommentForm" class="comment-form">
          <textarea
            v-model="newComment"
            placeholder="Оставьте ваш комментарий..."
            rows="3"
          ></textarea>
          <div class="comment-actions">
            <button class="btn btn-primary" @click="addComment">Отправить</button>
            <button class="btn btn-secondary" @click="showCommentForm = false">Отмена</button>
          </div>
        </div>

        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment">
            <img :src="comment.user.avatar" class="comment-avatar" alt="Avatar" />
            <div class="comment-content">
              <div class="comment-header">
                <span class="comment-user">{{ comment.user.name }}</span>
                <span class="comment-time">{{ comment.time }}</span>
              </div>
              <p class="comment-text">{{ comment.text }}</p>
              <div class="comment-actions">
                <button class="comment-action" @click="likeComment(comment.id)">
                  ❤️ {{ comment.likes }}
                </button>
                <button class="comment-action" @click="replyToComment(comment)">💬 Ответить</button>
                <button
                  v-if="comment.user.id === currentUserId"
                  class="comment-action"
                  @click="deleteComment(comment.id)"
                >
                  🗑️ Удалить
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Редактировать плейлист</h3>
          <button class="close-btn" @click="showEditModal = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Название</label>
            <input v-model="editForm.title" type="text" />
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="editForm.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>Обложка (URL)</label>
            <input v-model="editForm.cover" type="text" />
          </div>
          <div class="form-group">
            <label>Видимость</label>
            <div class="visibility-options">
              <label>
                <input v-model="editForm.isPublic" type="radio" :value="true" />
                <span>Публичный</span>
              </label>
              <label>
                <input v-model="editForm.isPublic" type="radio" :value="false" />
                <span>Приватный</span>
              </label>
            </div>
          </div>
          <div class="modal-actions">
            <button class="btn btn-primary" @click="saveChanges">Сохранить</button>
            <button class="btn btn-secondary" @click="showEditModal = false">Отмена</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlaylistDetailView',
  data() {
    return {
      playlist: {
        id: this.$route.params.id,
        title: 'Лучшие хиты 2024',
        description: 'Самые популярные треки этого года. Обновляется еженедельно.',
        cover: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=800&fit=crop',
        creator: 'Музыкальный редактор',
        createdAt: '15 января 2024',
        duration: 4567,
        likes: 2345,
        plays: 15678,
        tags: ['2024', 'хиты', 'поп', 'новинки'],
        tracks: [],
      },
      tracks: [],
      filteredTracks: [],
      searchQuery: '',
      sortBy: 'title',
      loading: false,
      isPlaying: false,
      currentTrack: null,
      isSaved: false,
      isOwner: true,
      showCommentForm: false,
      newComment: '',
      comments: [],
      similarPlaylists: [],
      showEditModal: false,
      editForm: {
        title: '',
        description: '',
        cover: '',
        isPublic: true,
      },
      currentUserId: 1,
    }
  },
  computed: {
    formattedDuration() {
      return this.formatDuration(this.playlist.duration)
    },
  },
  async mounted() {
    await this.loadPlaylist()
    this.loadTracks()
    this.loadComments()
    this.loadSimilarPlaylists()
    this.checkIfSaved()
  },
  methods: {
    async loadPlaylist() {
      this.loading = true
      try {
        const response = await fetch(`/api/playlists/${this.playlist.id}`)
        const data = await response.json()
        if (data.success) {
          this.playlist = data.playlist
        }
      } catch (error) {
        console.error('Error loading playlist:', error)
        this.loadMockData()
      } finally {
        this.loading = false
      }
    },

    loadMockData() {
      this.playlist.tracks = [
        {
          id: 1,
          title: 'Blinding Lights',
          artist: 'The Weeknd',
          album: 'After Hours',
          cover:
            'https://i.scdn.co/image/ab67616d00001e02/86a0f12c8d1c65b6e6c8b1a0f2c5e8b1d5b3a8f2',
          duration: 200,
          added: '2 дня назад',
          isLiked: true,
        },
        {
          id: 2,
          title: 'Levitating',
          artist: 'Dua Lipa',
          album: 'Future Nostalgia',
          cover:
            'https://i.scdn.co/image/ab67616d00001e02/f2b8b5b5f5b5f5b5f5b5f5b5f5b5f5b5f5b5f5b5',
          duration: 203,
          added: 'неделю назад',
          isLiked: false,
        },
        {
          id: 3,
          title: 'Stay',
          artist: 'The Kid LAROI, Justin Bieber',
          album: 'F*CK LOVE 3',
          cover: 'https://i.scdn.co/image/ab67616d00001e02/6e0b5b8b9c5b8b8b8b8b8b8b8b8b8b8b8b8b8b8',
          duration: 141,
          added: '3 дня назад',
          isLiked: true,
        },
      ]

      this.tracks = [...this.playlist.tracks]
      this.filteredTracks = [...this.tracks]
    },

    loadTracks() {
      this.filteredTracks = [...this.tracks]
    },

    loadComments() {
      this.comments = [
        {
          id: 1,
          user: {
            id: 1,
            name: 'Алексей',
            avatar: 'https://i.pravatar.cc/150?img=1',
          },
          text: 'Отличный плейлист! Слушаю каждый день по пути на работу.',
          time: '2 часа назад',
          likes: 12,
        },
        {
          id: 2,
          user: {
            id: 2,
            name: 'Мария',
            avatar: 'https://i.pravatar.cc/150?img=5',
          },
          text: 'Не хватает треков Billie Eilish. Может добавите?',
          time: '5 часов назад',
          likes: 8,
        },
        {
          id: 3,
          user: {
            id: 3,
            name: 'Дмитрий',
            avatar: 'https://i.pravatar.cc/150?img=8',
          },
          text: 'Лучшая подборка этого года! Спасибо!',
          time: '1 день назад',
          likes: 24,
        },
      ]
    },

    loadSimilarPlaylists() {
      this.similarPlaylists = [
        {
          id: 2,
          title: 'Топ 100: Глобальный чарт',
          creator: 'Spotify',
          cover:
            'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300&h=300&fit=crop',
          tracks: 100,
          likes: 56789,
        },
        {
          id: 3,
          title: 'Русские хиты 2024',
          creator: 'Музыкальный блог',
          cover:
            'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=300&h=300&fit=crop',
          tracks: 50,
          likes: 12345,
        },
        {
          id: 4,
          title: 'Рабочий настрой',
          creator: 'Продуктивный день',
          cover:
            'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=300&h=300&fit=crop',
          tracks: 30,
          likes: 8765,
        },
      ]
    },

    checkIfSaved() {
      const savedPlaylists = JSON.parse(localStorage.getItem('saved_playlists') || '[]')
      this.isSaved = savedPlaylists.includes(this.playlist.id)
    },

    searchTracks() {
      if (!this.searchQuery) {
        this.filteredTracks = [...this.tracks]
        return
      }

      const query = this.searchQuery.toLowerCase()
      this.filteredTracks = this.tracks.filter(
        (track) =>
          track.title.toLowerCase().includes(query) ||
          track.artist.toLowerCase().includes(query) ||
          track.album.toLowerCase().includes(query),
      )
    },

    sortBy(criteria) {
      this.sortBy = criteria
      this.filteredTracks.sort((a, b) => {
        switch (criteria) {
          case 'title':
            return a.title.localeCompare(b.title)
          case 'artist':
            return a.artist.localeCompare(b.artist)
          case 'duration':
            return a.duration - b.duration
          case 'added':
            return new Date(b.added) - new Date(a.added)
          default:
            return 0
        }
      })
    },

    playPlaylist() {
      this.isPlaying = true
      this.currentTrack = this.filteredTracks[0]
      alert('Воспроизведение плейлиста начато')
    },

    playTrack(track) {
      this.isPlaying = true
      this.currentTrack = track
      alert(`Воспроизведение: ${track.title} - ${track.artist}`)
    },

    shufflePlaylist() {
      this.filteredTracks = [...this.tracks].sort(() => Math.random() - 0.5)
      alert('Плейлист перемешан')
    },

    toggleLikeTrack(track) {
      track.isLiked = !track.isLiked
      if (track.isLiked) {
        this.playlist.likes++
      } else {
        this.playlist.likes--
      }
    },

    addToQueue(track) {
      alert(`Трек "${track.title}" добавлен в очередь`)
    },

    removeFromPlaylist(trackId) {
      if (confirm('Удалить трек из плейлиста?')) {
        this.tracks = this.tracks.filter((t) => t.id !== trackId)
        this.filteredTracks = this.filteredTracks.filter((t) => t.id !== trackId)
        this.playlist.tracks = this.tracks
      }
    },

    savePlaylist() {
      this.isSaved = !this.isSaved
      const savedPlaylists = JSON.parse(localStorage.getItem('saved_playlists') || '[]')

      if (this.isSaved) {
        savedPlaylists.push(this.playlist.id)
        alert('Плейлист сохранен в избранное')
      } else {
        const index = savedPlaylists.indexOf(this.playlist.id)
        if (index > -1) {
          savedPlaylists.splice(index, 1)
        }
        alert('Плейлист удален из избранного')
      }

      localStorage.setItem('saved_playlists', JSON.stringify(savedPlaylists))
    },

    sharePlaylist() {
      const shareUrl = `${window.location.origin}/playlist/${this.playlist.id}`
      const text = `Слушай плейлист "${this.playlist.title}" на MusBlossom! 🎵`

      if (navigator.share) {
        navigator.share({
          title: this.playlist.title,
          text: text,
          url: shareUrl,
        })
      } else {
        navigator.clipboard.writeText(`${text}\n${shareUrl}`)
        alert('Ссылка на плейлист скопирована!')
      }
    },

    viewPlaylist(playlist) {
      this.$router.push(`/playlists/${playlist.id}`)
    },

    addComment() {
      if (this.newComment.trim()) {
        this.comments.unshift({
          id: Date.now(),
          user: {
            id: this.currentUserId,
            name: 'Вы',
            avatar: 'https://i.pravatar.cc/150?img=1',
          },
          text: this.newComment,
          time: 'только что',
          likes: 0,
        })
        this.newComment = ''
        this.showCommentForm = false
      }
    },

    likeComment(commentId) {
      const comment = this.comments.find((c) => c.id === commentId)
      if (comment) {
        comment.likes++
      }
    },

    replyToComment(comment) {
      this.newComment = `@${comment.user.name} `
      this.showCommentForm = true
    },

    deleteComment(commentId) {
      if (confirm('Удалить комментарий?')) {
        this.comments = this.comments.filter((c) => c.id !== commentId)
      }
    },

    formatDuration(seconds) {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      return hours > 0 ? `${hours} ч ${minutes} мин` : `${minutes} мин`
    },

    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${minutes}:${secs.toString().padStart(2, '0')}`
    },

    editPlaylist() {
      this.editForm = {
        title: this.playlist.title,
        description: this.playlist.description,
        cover: this.playlist.cover,
        isPublic: true,
      }
      this.showEditModal = true
    },

    saveChanges() {
      this.playlist.title = this.editForm.title
      this.playlist.description = this.editForm.description
      this.playlist.cover = this.editForm.cover
      this.showEditModal = false
      alert('Изменения сохранены')
    },
  },
}
</script>

<style scoped>
.playlist-detail-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.playlist-header {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 3rem;
  margin: 2rem 0 3rem;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.1), rgba(75, 0, 130, 0.1));
  border-radius: 15px;
}

.playlist-cover {
  position: relative;
}

.playlist-cover img {
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.playlist-actions {
  position: absolute;
  bottom: -20px;
  left: 0;
  right: 0;
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.play-btn {
  padding: 0.8rem 1.5rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  border: none;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.play-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.action-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.playlist-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.playlist-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  color: #b0b0b0;
  font-size: 0.9rem;
}

.playlist-title {
  font-size: 2.5rem;
  color: white;
  margin-bottom: 1rem;
}

.playlist-description {
  color: #b0b0b0;
  margin-bottom: 1.5rem;
  line-height: 1.6;
  font-size: 1.1rem;
}

.playlist-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  color: #888;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.playlist-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  padding: 0.3rem 0.8rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-radius: 15px;
  font-size: 0.9rem;
}

.playlist-content {
  margin-bottom: 3rem;
}

.playlist-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.search-box input {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 3rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-buttons button {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 20px;
  color: #b0b0b0;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.filter-buttons button:hover {
  background: rgba(138, 43, 226, 0.1);
  border-color: #8a2be2;
  color: #8a2be2;
}

.filter-buttons button.active {
  background: rgba(138, 43, 226, 0.2);
  border-color: #8a2be2;
  color: #8a2be2;
}

.tracks-list {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  overflow: hidden;
  margin-bottom: 3rem;
}

.tracks-header {
  display: grid;
  grid-template-columns: 50px 2fr 1fr 1fr 1fr 60px 100px;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.08);
  color: #b0b0b0;
  font-weight: 500;
  font-size: 0.9rem;
}

.loading {
  text-align: center;
  padding: 3rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(138, 43, 226, 0.3);
  border-radius: 50%;
  border-top-color: #8a2be2;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.tracks-container {
  max-height: 600px;
  overflow-y: auto;
}

.track-item {
  display: grid;
  grid-template-columns: 50px 2fr 1fr 1fr 1fr 60px 100px;
  gap: 1rem;
  padding: 1rem 1.5rem;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: background 0.3s;
  cursor: pointer;
}

.track-item:hover {
  background: rgba(255, 255, 255, 0.03);
}

.track-item.playing {
  background: rgba(138, 43, 226, 0.1);
}

.track-number {
  text-align: center;
  color: #888;
  font-weight: 500;
}

.playing-icon {
  color: #8a2be2;
}

.track-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.track-cover {
  width: 40px;
  height: 40px;
  border-radius: 5px;
  object-fit: cover;
}

.track-details h4 {
  color: white;
  margin-bottom: 0.2rem;
  font-size: 1rem;
}

.track-details p {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.track-artist-info,
.track-album,
.track-added {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.track-duration {
  color: #888;
  font-size: 0.9rem;
}

.track-actions {
  display: flex;
  gap: 0.3rem;
}

.no-tracks {
  text-align: center;
  padding: 4rem;
}

.no-tracks-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.no-tracks h3 {
  color: white;
  margin-bottom: 0.5rem;
}

.no-tracks p {
  color: #b0b0b0;
}

.similar-playlists {
  margin-bottom: 3rem;
}

.similar-playlists h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.playlists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.playlist-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.playlist-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
}

.playlist-img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.playlist-card-info {
  padding: 1rem;
}

.playlist-card-info h4 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.playlist-card-info p {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.playlist-card-stats {
  display: flex;
  justify-content: space-between;
  color: #888;
  font-size: 0.8rem;
}

.comments-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.comments-header h3 {
  color: white;
  font-size: 1.3rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: white;
  border: 1px solid #444;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.comment-form {
  margin-bottom: 2rem;
}

.comment-form textarea {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-family: inherit;
  resize: vertical;
  margin-bottom: 1rem;
}

.comment-actions {
  display: flex;
  gap: 1rem;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comment {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-user {
  color: white;
  font-weight: 500;
}

.comment-time {
  color: #888;
  font-size: 0.9rem;
}

.comment-text {
  color: #b0b0b0;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.comment-actions {
  display: flex;
  gap: 1rem;
}

.comment-action {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.comment-action:hover {
  color: white;
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
}

.modal-content {
  background: #1e1e2e;
  border-radius: 15px;
  width: 90%;
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

.modal-header h3 {
  color: white;
  font-size: 1.3rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  color: white;
  margin-bottom: 0.5rem;
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
  font-family: inherit;
}

.visibility-options {
  display: flex;
  gap: 1.5rem;
}

.visibility-options label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.visibility-options input {
  width: auto;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .playlist-header {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 2rem;
  }

  .playlist-actions {
    position: static;
    margin-top: 1rem;
  }

  .tracks-header,
  .track-item {
    grid-template-columns: 1fr;
    display: none;
  }

  .tracks-header {
    display: none;
  }

  .track-item {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
  }

  .track-info {
    width: 100%;
  }

  .track-actions {
    align-self: flex-end;
  }

  .playlists-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .playlist-controls {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .filter-buttons {
    justify-content: center;
  }

  .playlists-grid {
    grid-template-columns: 1fr;
  }
}
</style>
