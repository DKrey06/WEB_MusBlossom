<template>
  <div class="user-profile-view">
    <div class="profile-header">
      <div class="profile-info">
        <div class="profile-avatar">
          <img :src="user.avatar" alt="Avatar" />
          <div class="online-status" :class="{ online: user.isOnline }"></div>
        </div>
        <div class="profile-details">
          <div class="profile-name">
            <h1>{{ user.username }}</h1>
            <span class="user-badge" v-if="user.isVerified">✅</span>
            <span class="user-role">{{ user.role }}</span>
          </div>
          <p class="profile-bio">{{ user.bio }}</p>
          <div class="profile-stats">
            <div class="stat">
              <span class="stat-value">{{ user.stats.posts }}</span>
              <span class="stat-label">Постов</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ user.stats.followers }}</span>
              <span class="stat-label">Подписчиков</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ user.stats.following }}</span>
              <span class="stat-label">Подписок</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ user.stats.playlists }}</span>
              <span class="stat-label">Плейлистов</span>
            </div>
          </div>
          <div class="profile-actions">
            <button v-if="!isCurrentUser" class="btn btn-primary" @click="toggleFollow">
              {{ user.isFollowing ? '✅ Подписан' : '➕ Подписаться' }}
            </button>
            <button v-if="!isCurrentUser" class="btn btn-secondary" @click="sendMessage">
              Сообщение
            </button>
            <button
              v-if="!isCurrentUser && user.isFollowing"
              class="btn btn-secondary"
              @click="showMoreActions = !showMoreActions"
            >
              ⋮
            </button>
            <button
              v-if="isCurrentUser"
              class="btn btn-primary edit-profile-btn"
              @click="editProfile"
            >
              Редактировать профиль
            </button>
            <div v-if="showMoreActions" class="more-actions">
              <button @click="blockUser">Заблокировать</button>
              <button @click="reportUser">Пожаловаться</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="profile-content">
      <div class="profile-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="profile-main">
        <div v-if="activeTab === 'posts'" class="tab-content">
          <div v-if="user.posts.length" class="posts-grid">
            <div v-for="post in user.posts" :key="post.id" class="post-card">
              <div class="post-header">
                <div class="post-author">
                  <img :src="user.avatar" alt="Avatar" class="post-author-avatar" />
                  <span class="post-author-name">{{ user.username }}</span>
                </div>
                <span class="post-time">{{ post.time }}</span>
              </div>
              <h4 class="post-title">{{ post.title }}</h4>
              <p class="post-content">{{ post.content }}</p>
              <div class="post-stats">
                <span>{{ post.likes }}</span>
                <span>{{ post.comments }}</span>
                <span>{{ post.shares }}</span>
              </div>
            </div>
          </div>
          <div v-else class="no-content">
            <p>Пользователь еще не публиковал посты</p>
          </div>
        </div>

        <div v-if="activeTab === 'playlists'" class="tab-content">
          <div v-if="user.playlists.length" class="playlists-grid">
            <div
              v-for="playlist in user.playlists"
              :key="playlist.id"
              class="playlist-card"
              @click="viewPlaylist(playlist)"
            >
              <img :src="playlist.cover" alt="Cover" />
              <div class="playlist-info">
                <h4>{{ playlist.name }}</h4>
                <p>{{ playlist.tracks }} треков</p>
                <span>{{ playlist.likes }}</span>
              </div>
            </div>
          </div>
          <div v-else class="no-content">
            <p>У пользователя нет публичных плейлистов</p>
          </div>
        </div>

        <div v-if="activeTab === 'likes'" class="tab-content">
          <div v-if="user.likes.length" class="likes-grid">
            <div v-for="like in user.likes" :key="like.id" class="like-card">
              <img :src="like.cover" alt="Cover" />
              <div class="like-info">
                <h4>{{ like.title }}</h4>
                <p>{{ like.artist }}</p>
                <span class="like-date">{{ like.date }}</span>
              </div>
            </div>
          </div>
          <div v-else class="no-content">
            <p>Пользователь еще не ставил лайки</p>
          </div>
        </div>

        <div v-if="activeTab === 'about'" class="tab-content">
          <div class="about-section">
            <h3>О себе</h3>
            <p class="about-text">{{ user.about }}</p>
          </div>
          <div class="about-section">
            <h3>На MusBlossom с</h3>
            <p>{{ user.joinedDate }}</p>
          </div>
          <div class="about-section">
            <h3>Местоположение</h3>
            <p>{{ user.location }}</p>
          </div>
          <div class="about-section">
            <h3>Любимые исполнители</h3>
            <div class="favorite-artists">
              <div v-for="artist in user.favoriteArtists" :key="artist" class="artist">
                {{ artist }}
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
  name: 'UserProfileView',
  data() {
    return {
      user: {
        id: parseInt(this.$route.params.id) || 1,
        username: 'Алексей Рокер',
        avatar: require('@/assets/images/Avatar.jpg'),
        bio: 'Люблю рок-музыку, играю на гитаре. Слушаю все от классики до современных хитов.',
        isOnline: true,
        isVerified: true,
        role: 'Премиум пользователь',
        stats: {
          posts: 45,
          followers: 2345,
          following: 189,
          playlists: 12,
        },
        posts: [
          {
            id: 1,
            type: 'Рецензия',
            title: 'Новый альбом Arctic Monkeys',
            content: 'Отличный альбом, чувствуется эволюция группы...',
            time: '2 дня назад',
            likes: 45,
            comments: 12,
            shares: 3,
          },
          {
            id: 2,
            type: 'Мысли',
            title: 'О важности живых концертов',
            content: 'Ничто не заменит энергию живого выступления...',
            time: 'неделю назад',
            likes: 89,
            comments: 23,
            shares: 7,
          },
        ],
        playlists: [
          {
            id: 1,
            name: 'Лучший рок 80-х',
            cover:
              'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300&h=300&fit=crop',
            tracks: 25,
            likes: 234,
          },
          {
            id: 2,
            name: 'Для работы',
            cover:
              'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=300&h=300&fit=crop',
            tracks: 30,
            likes: 156,
          },
        ],
        likes: [
          {
            id: 1,
            title: 'Bohemian Rhapsody',
            artist: 'Queen',
            cover:
              'https://i.scdn.co/image/ab67616d00001e02/1c7b0c5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5',
            date: 'вчера',
          },
          {
            id: 2,
            title: 'Stairway to Heaven',
            artist: 'Led Zeppelin',
            cover:
              'https://i.scdn.co/image/ab67616d00001e02/2c7b0c5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5b5',
            date: '3 дня назад',
          },
        ],
        about:
          'Музыкант с 10-летним стажем. Люблю исследовать новые жанры и делиться открытиями с другими.',
        joinedDate: 'Январь 2022',
        location: 'Москва, Россия',
        favoriteArtists: ['Arctic Monkeys', 'Queen', 'Led Zeppelin', 'The Beatles', 'Nirvana'],
        isFollowing: false,
      },
      activeTab: 'posts',
      showMoreActions: false,
      tabs: [
        { id: 'posts', label: 'Посты' },
        { id: 'playlists', label: 'Плейлисты' },
        { id: 'likes', label: 'Лайки' },
        { id: 'about', label: 'О пользователе' },
      ],
      currentUserId: 1,
    }
  },
  computed: {
    isCurrentUser() {
      return this.user.id === this.currentUserId
    },
  },
  async mounted() {
    await this.loadUserProfile()
  },
  methods: {
    async loadUserProfile() {
      const userId = this.$route.params.id
      try {
        const response = await fetch(`/api/users/${userId}`)
        const data = await response.json()
        if (data.success) {
          this.user = data.user
        }
      } catch (error) {
        console.error('Error loading user profile:', error)
      }
    },

    toggleFollow() {
      this.user.isFollowing = !this.user.isFollowing
      if (this.user.isFollowing) {
        this.user.stats.followers++
        alert(`Вы подписались на ${this.user.username}`)
      } else {
        this.user.stats.followers--
        alert(`Вы отписались от ${this.user.username}`)
      }
    },

    sendMessage() {
      alert(`Открыть чат с ${this.user.username}`)
    },

    blockUser() {
      if (confirm(`Заблокировать ${this.user.username}?`)) {
        alert(`${this.user.username} заблокирован`)
        this.showMoreActions = false
      }
    },

    reportUser() {
      alert(`Жалоба на ${this.user.username} отправлена`)
      this.showMoreActions = false
    },

    editProfile() {
      alert('Редактирование профиля')
    },

    viewPlaylist(playlist) {
      this.$router.push(`/playlists/${playlist.id}`)
    },
  },
}
</script>

<style scoped>
.user-profile-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.profile-header {
  position: relative;
  margin-bottom: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.1), rgba(75, 0, 130, 0.1));
  border-radius: 15px;
}

.profile-info {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.profile-avatar {
  position: relative;
  flex-shrink: 0;
}

.profile-avatar img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid rgba(255, 255, 255, 0.1);
}

.online-status {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 20px;
  height: 20px;
  background: #888;
  border-radius: 50%;
  border: 3px solid #1a1a2e;
}

.online-status.online {
  background: #2ed573;
}

.profile-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.profile-name {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.profile-name h1 {
  font-size: 2rem;
  color: white;
  margin: 0;
  line-height: 1.2;
}

.user-badge {
  font-size: 1.2rem;
}

.user-role {
  padding: 0.3rem 0.8rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-radius: 15px;
  font-size: 0.9rem;
}

.profile-bio {
  color: #b0b0b0;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  line-height: 1.5;
}

.profile-stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #8a2be2;
  margin-bottom: 0.3rem;
}

.stat-label {
  color: #888;
  font-size: 0.9rem;
}

.profile-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-top: auto;
  position: relative;
}

.edit-profile-btn {
  margin-left: auto;
}

.btn {
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  white-space: nowrap;
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

.more-actions {
  position: absolute;
  top: 100%;
  right: 0;
  background: #1a1a2e;
  border: 1px solid #333;
  border-radius: 10px;
  padding: 0.5rem;
  min-width: 150px;
  z-index: 10;
}

.more-actions button {
  display: block;
  width: 100%;
  padding: 0.8rem;
  background: none;
  border: none;
  color: #b0b0b0;
  text-align: left;
  cursor: pointer;
  border-radius: 5px;
}

.more-actions button:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-tabs {
  display: flex;
  gap: 0;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  overflow: hidden;
}

.profile-tabs button {
  flex: 1;
  padding: 1rem;
  background: transparent;
  border: none;
  color: #b0b0b0;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
  font-size: 1rem;
}

.profile-tabs button:hover {
  background: rgba(255, 255, 255, 0.05);
}

.profile-tabs button.active {
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
}

.profile-main {
  min-height: 500px;
}

.tab-content {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 1.5rem;
}

.no-content {
  text-align: center;
  padding: 3rem;
  color: #888;
}

.posts-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.post-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1.5rem;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.post-author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.post-author-name {
  color: white;
  font-weight: 500;
  font-size: 1rem;
}

.post-time {
  color: #888;
  font-size: 0.9rem;
}

.post-title {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.post-content {
  color: #b0b0b0;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.post-stats {
  display: flex;
  gap: 1.5rem;
  color: #888;
  font-size: 0.9rem;
}

.playlists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.playlist-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.playlist-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.05);
}

.playlist-card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.playlist-info {
  padding: 1rem;
}

.playlist-info h4 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.playlist-info p {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.playlist-info span {
  color: #888;
  font-size: 0.8rem;
}

.likes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.like-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  overflow: hidden;
}

.like-card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.like-info {
  padding: 1rem;
}

.like-info h4 {
  color: white;
  margin-bottom: 0.3rem;
  font-size: 1rem;
}

.like-info p {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.like-date {
  color: #888;
  font-size: 0.8rem;
}

.about-section {
  margin-bottom: 2rem;
}

.about-section h3 {
  color: white;
  margin-bottom: 0.8rem;
  font-size: 1.2rem;
}

.about-text {
  color: #b0b0b0;
  line-height: 1.6;
}

.about-section p {
  color: #b0b0b0;
}

.favorite-artists {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.artist {
  padding: 0.5rem 1rem;
  background: rgba(138, 43, 226, 0.1);
  color: #8a2be2;
  border-radius: 20px;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .profile-info {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .profile-avatar img {
    width: 120px;
    height: 120px;
  }

  .profile-name {
    justify-content: center;
  }

  .profile-name h1 {
    font-size: 1.8rem;
  }

  .profile-stats {
    justify-content: center;
    flex-wrap: wrap;
  }

  .profile-actions {
    justify-content: center;
    flex-wrap: wrap;
  }

  .edit-profile-btn {
    margin-left: 0;
  }

  .profile-tabs {
    flex-wrap: wrap;
  }

  .profile-tabs button {
    min-width: 120px;
  }

  .playlists-grid,
  .likes-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  .post-author-avatar {
    width: 35px;
    height: 35px;
  }
}

@media (max-width: 480px) {
  .profile-header {
    padding: 1.5rem;
  }

  .profile-name h1 {
    font-size: 1.5rem;
  }

  .btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }

  .tab-content {
    padding: 1rem;
  }

  .playlists-grid,
  .likes-grid {
    grid-template-columns: 1fr;
  }
}
</style>
