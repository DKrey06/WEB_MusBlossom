<template>
  <div class="music-room-view">
    <div class="room-container">
      <div class="room-sidebar">
        <div class="room-info">
          <h2>{{ room.name }}</h2>
          <p class="room-description">{{ room.description }}</p>
          <div class="room-stats">
            <span class="stat">🎧 {{ room.listeners }} слушают</span>
            <span class="stat">👥 {{ room.participants.length }} в комнате</span>
            <span class="stat">🎵 {{ room.queue.length }} в очереди</span>
          </div>
        </div>

        <div class="participants-list">
          <h3>Участники</h3>
          <div class="participants">
            <div v-for="user in room.participants" :key="user.id" class="participant">
              <img :src="user.avatar" class="user-avatar" alt="Avatar" />
              <div class="user-info">
                <span class="username">{{ user.username }}</span>
                <span class="user-role" :class="user.role">{{ user.role }}</span>
                <div v-if="user.isSpeaking" class="speaking-indicator"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="room-chat">
          <h3>Чат комнаты</h3>
          <div class="chat-messages" ref="chatMessages">
            <div v-for="message in messages" :key="message.id" class="message">
              <img :src="message.user.avatar" class="message-avatar" alt="Avatar" />
              <div class="message-content">
                <span class="message-user">{{ message.user.username }}</span>
                <span class="message-text">{{ message.text }}</span>
                <span class="message-time">{{ message.time }}</span>
              </div>
            </div>
          </div>
          <div class="chat-input">
            <input
              type="text"
              v-model="newMessage"
              placeholder="Напишите сообщение..."
              @keyup.enter="sendMessage"
            />
            <button class="send-btn" @click="sendMessage">📤</button>
          </div>
        </div>
      </div>

      <div class="room-main">
        <div class="current-track">
          <div class="track-cover">
            <img :src="currentTrack.cover" alt="Cover" />
            <div class="track-overlay">
              <span class="track-status" v-if="isPlaying">▶️ Воспроизводится</span>
              <span class="track-status" v-else>⏸️ На паузе</span>
            </div>
          </div>
          <div class="track-info">
            <h3 class="track-title">{{ currentTrack.title }}</h3>
            <p class="track-artist">{{ currentTrack.artist }}</p>
            <div class="track-progress">
              <div class="progress-bar" @click="seekTrack">
                <div class="progress-fill" :style="{ width: progress + '%' }"></div>
              </div>
              <div class="progress-time">
                <span>{{ formatTime(currentTime) }}</span>
                <span>{{ formatTime(currentTrack.duration) }}</span>
              </div>
            </div>
            <div class="track-controls">
              <button class="control-btn" @click="prevTrack">⏮️</button>
              <button class="control-btn play-btn" @click="togglePlay">
                {{ isPlaying ? '⏸️' : '▶️' }}
              </button>
              <button class="control-btn" @click="nextTrack">⏭️</button>
              <button class="control-btn" @click="toggleLike">
                {{ isLiked ? '❤️' : '🤍' }}
              </button>
              <button class="control-btn" @click="addToPlaylist">➕</button>
              <div class="volume-control">
                <button class="volume-btn" @click="toggleMute">
                  {{ isMuted ? '🔇' : '🔊' }}
                </button>
                <input type="range" v-model="volume" min="0" max="100" class="volume-slider" />
              </div>
            </div>
          </div>
        </div>

        <div class="queue-section">
          <div class="queue-header">
            <h3>🎵 Очередь воспроизведения</h3>
            <button class="btn btn-small" @click="addToQueue">Добавить трек</button>
          </div>
          <div class="queue-list">
            <div
              v-for="(track, index) in room.queue"
              :key="track.id"
              class="queue-item"
              :class="{ current: index === 0 }"
            >
              <div class="queue-number">{{ index + 1 }}</div>
              <img :src="track.cover" class="queue-cover" alt="Cover" />
              <div class="queue-info">
                <h4>{{ track.title }}</h4>
                <p>{{ track.artist }}</p>
                <span class="queue-duration">{{ formatTime(track.duration) }}</span>
              </div>
              <div class="queue-actions">
                <button class="action-btn" @click="voteTrack(track.id, 'up')">👍</button>
                <span class="vote-count">{{ track.votes }}</span>
                <button class="action-btn" @click="voteTrack(track.id, 'down')">👎</button>
                <button
                  v-if="currentUser.role === 'host' || currentUser.id === track.addedBy"
                  class="action-btn"
                  @click="removeFromQueue(track.id)"
                >
                  🗑️
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="room-features">
          <div class="feature">
            <h3>🎮 Интерактивные игры</h3>
            <div class="games-list">
              <button class="game-btn" @click="startGame('guess-melody')">Угадай мелодию</button>
              <button class="game-btn" @click="startGame('guess-lyrics')">Угадай текст</button>
              <button class="game-btn" @click="startGame('trivia')">Музыкальная викторина</button>
            </div>
          </div>

          <div class="feature">
            <h3>📊 Статистика комнаты</h3>
            <div class="stats-grid">
              <div class="stat-item">
                <span class="stat-value">{{ room.stats.totalTracks }}</span>
                <span class="stat-label">Проиграно треков</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ room.stats.totalTime }}</span>
                <span class="stat-label">Часов музыки</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ room.stats.topGenre }}</span>
                <span class="stat-label">Популярный жанр</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ room.stats.activeUsers }}</span>
                <span class="stat-label">Активных слушателей</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="currentUser.role === 'host'" class="room-management">
          <h3>⚙️ Управление комнатой</h3>
          <div class="management-actions">
            <button class="btn btn-small" @click="changeRoomSettings">Настройки комнаты</button>
            <button class="btn btn-small" @click="manageParticipants">
              Управление участниками
            </button>
            <button class="btn btn-small" @click="exportPlaylist">Экспорт плейлиста</button>
            <button class="btn btn-small btn-danger" @click="closeRoom">Закрыть комнату</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showAddTrackModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Добавить трек в очередь</h3>
          <button class="close-btn" @click="showAddTrackModal = false">✕</button>
        </div>
        <div class="modal-body">
          <input
            type="text"
            v-model="searchTrack"
            placeholder="Поиск трека..."
            @input="searchTracks"
          />
          <div v-if="searchResults.length" class="search-results">
            <div
              v-for="track in searchResults"
              :key="track.id"
              class="search-result"
              @click="selectTrack(track)"
            >
              <img :src="track.cover" class="result-cover" alt="Cover" />
              <div class="result-info">
                <h4>{{ track.title }}</h4>
                <p>{{ track.artist }}</p>
                <span>{{ formatTime(track.duration) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MusicRoomView',
  data() {
    return {
      room: {
        id: this.$route.params.roomId,
        name: 'Вечеринка #1',
        description: 'Слушаем новинки и классику',
        listeners: 42,
        participants: [
          {
            id: 1,
            username: 'Алексей',
            avatar: 'https://i.pravatar.cc/150?img=1',
            role: 'host',
            isSpeaking: true,
          },
          {
            id: 2,
            username: 'Мария',
            avatar: 'https://i.pravatar.cc/150?img=5',
            role: 'speaker',
            isSpeaking: true,
          },
          {
            id: 3,
            username: 'Дмитрий',
            avatar: 'https://i.pravatar.cc/150?img=8',
            role: 'listener',
            isSpeaking: false,
          },
          {
            id: 4,
            username: 'Анна',
            avatar: 'https://i.pravatar.cc/150?img=4',
            role: 'listener',
            isSpeaking: false,
          },
        ],
        queue: [
          {
            id: 1,
            title: 'Blinding Lights',
            artist: 'The Weeknd',
            cover:
              'https://i.scdn.co/image/ab67616d00001e02/86a0f12c8d1c65b6e6c8b1a0f2c5e8b1d5b3a8f2',
            duration: 200,
            votes: 15,
            addedBy: 1,
          },
          {
            id: 2,
            title: 'Levitating',
            artist: 'Dua Lipa',
            cover:
              'https://i.scdn.co/image/ab67616d00001e02/f2b8b5b5f5b5f5b5f5b5f5b5f5b5f5b5f5b5f5b5',
            duration: 203,
            votes: 12,
            addedBy: 2,
          },
          {
            id: 3,
            title: 'Stay',
            artist: 'The Kid LAROI, Justin Bieber',
            cover:
              'https://i.scdn.co/image/ab67616d00001e02/6e0b5b8b9c5b8b8b8b8b8b8b8b8b8b8b8b8b8b8',
            duration: 141,
            votes: 8,
            addedBy: 3,
          },
        ],
        stats: {
          totalTracks: 156,
          totalTime: '24:30',
          topGenre: 'Поп',
          activeUsers: 28,
        },
      },
      currentTrack: {
        id: 1,
        title: 'Blinding Lights',
        artist: 'The Weeknd',
        cover: 'https://i.scdn.co/image/ab67616d00001e02/86a0f12c8d1c65b6e6c8b1a0f2c5e8b1d5b3a8f2',
        duration: 200,
      },
      messages: [
        {
          id: 1,
          user: {
            id: 1,
            username: 'Алексей',
            avatar: 'https://i.pravatar.cc/150?img=1',
          },
          text: 'Привет всем! Как вам этот трек?',
          time: '19:30',
        },
        {
          id: 2,
          user: {
            id: 2,
            username: 'Мария',
            avatar: 'https://i.pravatar.cc/150?img=5',
          },
          text: 'Отличный выбор! Люблю The Weeknd',
          time: '19:31',
        },
        {
          id: 3,
          user: {
            id: 3,
            username: 'Дмитрий',
            avatar: 'https://i.pravatar.cc/150?img=8',
          },
          text: 'Может следующий трек будет что-то из 80-х?',
          time: '19:32',
        },
      ],
      newMessage: '',
      isPlaying: true,
      isLiked: false,
      isMuted: false,
      currentTime: 45,
      progress: 22.5,
      volume: 80,
      showAddTrackModal: false,
      searchTrack: '',
      searchResults: [],
      currentUser: {
        id: 1,
        username: 'Алексей',
        avatar: 'https://i.pravatar.cc/150?img=1',
        role: 'host',
      },
      audioPlayer: null,
    }
  },
  computed: {
    formattedListeners() {
      return this.room.listeners.toLocaleString()
    },
  },
  mounted() {
    this.setupAudioPlayer()
    this.scrollToBottom()
    this.startRoomUpdates()
  },
  beforeUnmount() {
    this.cleanupRoom()
  },
  methods: {
    setupAudioPlayer() {
      this.audioPlayer = {
        play: () => (this.isPlaying = true),
        pause: () => (this.isPlaying = false),
        currentTime: 45,
        duration: 200,
      }
    },

    togglePlay() {
      this.isPlaying = !this.isPlaying
      if (this.isPlaying) {
        this.audioPlayer?.play()
      } else {
        this.audioPlayer?.pause()
      }
    },

    prevTrack() {
      if (this.room.queue.length > 1) {
        const prevTrack = this.room.queue[1]
        this.currentTrack = prevTrack
        this.room.queue = [prevTrack, ...this.room.queue.slice(2)]
        this.resetProgress()
      }
    },

    nextTrack() {
      if (this.room.queue.length > 1) {
        const nextTrack = this.room.queue[1]
        this.currentTrack = nextTrack
        this.room.queue = this.room.queue.slice(1)
        this.resetProgress()
      }
    },

    resetProgress() {
      this.currentTime = 0
      this.progress = 0
      this.updateProgress()
    },

    updateProgress() {
      if (this.isPlaying) {
        this.currentTime += 1
        this.progress = (this.currentTime / this.currentTrack.duration) * 100

        if (this.currentTime >= this.currentTrack.duration) {
          this.nextTrack()
        }

        setTimeout(this.updateProgress, 1000)
      }
    },

    seekTrack(event) {
      const progressBar = event.currentTarget
      const clickPosition = event.offsetX
      const barWidth = progressBar.offsetWidth
      const percentage = (clickPosition / barWidth) * 100

      this.progress = percentage
      this.currentTime = (this.currentTrack.duration * percentage) / 100
    },

    toggleLike() {
      this.isLiked = !this.isLiked
    },

    toggleMute() {
      this.isMuted = !this.isMuted
      this.volume = this.isMuted ? 0 : 80
    },

    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${minutes}:${secs.toString().padStart(2, '0')}`
    },

    sendMessage() {
      if (this.newMessage.trim()) {
        this.messages.push({
          id: Date.now(),
          user: this.currentUser,
          text: this.newMessage,
          time: new Date().toLocaleTimeString('ru-RU', {
            hour: '2-digit',
            minute: '2-digit',
          }),
        })
        this.newMessage = ''
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }
    },

    scrollToBottom() {
      const container = this.$refs.chatMessages
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },

    addToQueue() {
      this.showAddTrackModal = true
    },

    searchTracks() {
      if (this.searchTrack.length < 2) {
        this.searchResults = []
        return
      }

      this.searchResults = [
        {
          id: 4,
          title: 'As It Was',
          artist: 'Harry Styles',
          cover: 'https://i.scdn.co/image/ab67616d00001e02/7c2a5b8b9c5b8b8b8b8b8b8b8b8b8b8b8b8b8b8',
          duration: 167,
        },
        {
          id: 5,
          title: 'Bad Habit',
          artist: 'Steve Lacy',
          cover: 'https://i.scdn.co/image/ab67616d00001e02/8c2a5b8b9c5b8b8b8b8b8b8b8b8b8b8b8b8b8b8',
          duration: 189,
        },
        {
          id: 6,
          title: 'Anti-Hero',
          artist: 'Taylor Swift',
          cover: 'https://i.scdn.co/image/ab67616d00001e02/9c2a5b8b9c5b8b8b8b8b8b8b8b8b8b8b8b8b8b8',
          duration: 201,
        },
      ]
    },

    selectTrack(track) {
      this.room.queue.push({
        ...track,
        votes: 0,
        addedBy: this.currentUser.id,
      })
      this.showAddTrackModal = false
      this.searchTrack = ''
      this.searchResults = []
    },

    voteTrack(trackId, voteType) {
      const track = this.room.queue.find((t) => t.id === trackId)
      if (track) {
        if (voteType === 'up') {
          track.votes++
        } else {
          track.votes--
        }

        this.room.queue.sort((a, b) => b.votes - a.votes)
      }
    },

    removeFromQueue(trackId) {
      this.room.queue = this.room.queue.filter((t) => t.id !== trackId)
    },

    startGame(gameType) {
      alert(`Начинаем игру: ${gameType}`)
    },

    changeRoomSettings() {
      alert('Открыть настройки комнаты')
    },

    manageParticipants() {
      alert('Управление участниками')
    },

    exportPlaylist() {
      const playlist = {
        name: this.room.name,
        tracks: this.room.queue.map((t) => ({
          title: t.title,
          artist: t.artist,
          duration: t.duration,
        })),
      }

      const dataStr = JSON.stringify(playlist, null, 2)
      const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr)

      const link = document.createElement('a')
      link.setAttribute('href', dataUri)
      link.setAttribute('download', `${this.room.name}_playlist.json`)
      link.click()

      alert('Плейлист экспортирован!')
    },

    closeRoom() {
      if (confirm('Вы уверены, что хотите закрыть комнату?')) {
        this.$router.push('/')
      }
    },

    startRoomUpdates() {
      setInterval(() => {
        this.room.listeners += Math.floor(Math.random() * 3) - 1
        if (this.room.listeners < 1) this.room.listeners = 1
      }, 10000)
    },

    cleanupRoom() {
      clearInterval(this.roomUpdateInterval)
    },

    addToPlaylist() {
      alert('Добавить текущий трек в плейлист')
    },
  },
}
</script>

<style scoped>
.music-room-view {
  height: calc(100vh - 80px);
  overflow: hidden;
}

.room-container {
  display: grid;
  grid-template-columns: 350px 1fr;
  height: 100%;
  gap: 0;
}

.room-sidebar {
  background: rgba(255, 255, 255, 0.05);
  border-right: 1px solid #333;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: auto;
}

.room-info {
  padding: 1.5rem;
  border-bottom: 1px solid #333;
}

.room-info h2 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.room-description {
  color: #b0b0b0;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.room-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #888;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.participants-list {
  padding: 1.5rem;
  border-bottom: 1px solid #333;
  flex-shrink: 0;
}

.participants-list h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.participants {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.participant {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  flex: 1;
}

.username {
  display: block;
  color: white;
  font-weight: 500;
  margin-bottom: 0.2rem;
}

.user-role {
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
}

.user-role.host {
  background: rgba(255, 71, 87, 0.2);
  color: #ff4757;
}

.user-role.speaker {
  background: rgba(30, 144, 255, 0.2);
  color: #1e90ff;
}

.speaking-indicator {
  position: absolute;
  left: 35px;
  top: 35px;
  width: 10px;
  height: 10px;
  background: #2ed573;
  border-radius: 50%;
  border: 2px solid #1a1a2e;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

.room-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 300px;
}

.room-chat h3 {
  padding: 1.5rem 1.5rem 0.5rem;
  color: white;
  font-size: 1.1rem;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 0 1.5rem;
}

.message {
  display: flex;
  gap: 0.8rem;
  margin-bottom: 1rem;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
}

.message-user {
  display: block;
  color: white;
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 0.2rem;
}

.message-text {
  display: block;
  color: #b0b0b0;
  font-size: 0.95rem;
  margin-bottom: 0.2rem;
  line-height: 1.4;
}

.message-time {
  color: #888;
  font-size: 0.8rem;
}

.chat-input {
  padding: 1.5rem;
  border-top: 1px solid #333;
  display: flex;
  gap: 0.5rem;
}

.chat-input input {
  flex: 1;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 0.95rem;
}

.send-btn {
  padding: 0.8rem 1.2rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1rem;
}

.room-main {
  padding: 1.5rem;
  overflow-y: auto;
}

.current-track {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.track-cover {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
}

.track-cover img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.track-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  padding: 0.8rem;
  color: white;
  font-weight: 500;
}

.track-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.track-title {
  font-size: 2rem;
  color: white;
  margin-bottom: 0.5rem;
}

.track-artist {
  color: #8a2be2;
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.track-progress {
  margin-bottom: 2rem;
}

.progress-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  cursor: pointer;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  border-radius: 3px;
  transition: width 0.3s;
}

.progress-time {
  display: flex;
  justify-content: space-between;
  color: #888;
  font-size: 0.9rem;
}

.track-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.control-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  color: white;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: scale(1.05);
}

.control-btn.play-btn {
  width: 60px;
  height: 60px;
  font-size: 1.5rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: auto;
}

.volume-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.2rem;
}

.volume-slider {
  width: 100px;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #8a2be2;
  cursor: pointer;
}

.queue-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.queue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.queue-header h3 {
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

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.queue-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  max-height: 400px;
  overflow-y: auto;
}

.queue-item {
  display: grid;
  grid-template-columns: auto auto 1fr auto;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  transition: all 0.3s;
}

.queue-item.current {
  background: rgba(138, 43, 226, 0.1);
  border-left: 3px solid #8a2be2;
}

.queue-number {
  color: #888;
  font-size: 1.2rem;
  font-weight: bold;
  width: 30px;
  text-align: center;
}

.queue-cover {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  object-fit: cover;
}

.queue-info h4 {
  color: white;
  margin-bottom: 0.3rem;
  font-size: 1rem;
}

.queue-info p {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.queue-duration {
  color: #888;
  font-size: 0.8rem;
}

.queue-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  color: #b0b0b0;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.vote-count {
  color: white;
  font-weight: bold;
  min-width: 20px;
  text-align: center;
}

.room-features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.feature {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
}

.feature h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.games-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.game-btn {
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid #444;
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  transition: all 0.3s;
  text-align: left;
}

.game-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #8a2be2;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.room-management {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
}

.room-management h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.management-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-danger {
  background: rgba(255, 71, 87, 0.2);
  color: #ff4757;
  border: 1px solid rgba(255, 71, 87, 0.3);
}

.btn-danger:hover {
  background: rgba(255, 71, 87, 0.3);
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

.modal-body input {
  width: 100%;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.search-results {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 300px;
  overflow-y: auto;
}

.search-result {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s;
}

.search-result:hover {
  background: rgba(255, 255, 255, 0.05);
}

.result-cover {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  object-fit: cover;
}

.result-info h4 {
  color: white;
  margin-bottom: 0.3rem;
  font-size: 1rem;
}

.result-info p {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.result-info span {
  color: #888;
  font-size: 0.8rem;
}

@media (max-width: 1024px) {
  .room-container {
    grid-template-columns: 1fr;
    overflow-y: auto;
  }

  .room-sidebar {
    height: auto;
    border-right: none;
    border-bottom: 1px solid #333;
  }

  .current-track {
    grid-template-columns: 1fr;
  }

  .room-features {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .track-controls {
    flex-wrap: wrap;
    justify-content: center;
  }

  .volume-control {
    margin-left: 0;
    justify-content: center;
    width: 100%;
  }

  .queue-item {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .queue-actions {
    justify-content: center;
  }
}
</style>
