<template>
  <div class="profile-view">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>

    <div v-else class="profile-container">
      <div class="profile-header">
        <div class="cover-photo">
          <div class="cover-overlay"></div>
          <button v-if="isOwnProfile" class="edit-cover-btn" @click="editCover">
            ✏️ Изменить обложку
          </button>
        </div>

        <div class="profile-info">
          <div class="avatar-section">
            <img :src="user.avatar || defaultAvatar" class="profile-avatar" alt="Avatar" />
            <button v-if="isOwnProfile" class="edit-avatar-btn" @click="editAvatar">✏️</button>
          </div>

          <div class="profile-details">
            <h1 class="profile-name">{{ user.username }}</h1>
            <p v-if="user.bio" class="profile-bio">{{ user.bio }}</p>

            <div class="profile-stats">
              <div class="stat">
                <span class="stat-value">{{ stats.posts || 0 }}</span>
                <span class="stat-label">Постов</span>
              </div>
              <div class="stat">
                <span class="stat-value">{{ stats.followers || 0 }}</span>
                <span class="stat-label">Подписчиков</span>
              </div>
              <div class="stat">
                <span class="stat-value">{{ stats.following || 0 }}</span>
                <span class="stat-label">Подписок</span>
              </div>
              <div class="stat">
                <span class="stat-value">{{ stats.friends || 0 }}</span>
                <span class="stat-label">Друзей</span>
              </div>
            </div>

            <div class="profile-actions">
              <button v-if="!isOwnProfile" class="btn-action follow-btn" @click="toggleFollow">
                {{ isFollowing ? '✓ Подписан' : 'Подписаться' }}
              </button>
              <button v-if="!isOwnProfile" class="btn-action message-btn" @click="sendMessage">
                ✉️ Сообщение
              </button>
              <router-link v-if="isOwnProfile" to="/settings" class="btn-action edit-btn">
                ✏️ Редактировать профиль
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div class="profile-content">
        <aside class="profile-sidebar">
          <div class="sidebar-section">
            <h3>Информация</h3>

            <div class="info-item">
              <span class="info-label">Любимые жанры</span>
              <div class="info-value">
                <div v-if="user.genres && user.genres.length" class="genres-list">
                  <span v-for="genre in user.genres" :key="genre" class="genre-tag">
                    {{ genre }}
                  </span>
                </div>
                <span v-else class="no-info">Не указаны</span>
              </div>
            </div>

            <div class="info-item">
              <span class="info-label">На сайте с</span>
              <span class="info-value">{{ formatDate(user.created_at) }}</span>
            </div>

            <div class="info-item" v-if="user.location">
              <span class="info-label">Местоположение</span>
              <span class="info-value">{{ user.location }}</span>
            </div>

            <div class="info-item" v-if="user.website">
              <span class="info-label">Веб-сайт</span>
              <a :href="user.website" target="_blank" class="info-link">
                {{ user.website }}
              </a>
            </div>
          </div>
          <div v-if="user.playlists && user.playlists.length" class="sidebar-section">
            <h3>Плейлисты</h3>
            <div class="playlists-preview">
              <div
                v-for="playlist in user.playlists.slice(0, 3)"
                :key="playlist.id"
                class="playlist-item"
                @click="$router.push(`/playlists/${playlist.id}`)"
              >
                <div class="playlist-cover" :style="{ backgroundImage: `url(${playlist.cover})` }">
                  <span class="playlist-count">{{ playlist.tracks_count }} треков</span>
                </div>
                <span class="playlist-name">{{ playlist.name }}</span>
              </div>
            </div>
          </div>
        </aside>

        <main class="profile-feed">
          <div class="feed-tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              :class="{ active: activeTab === tab.id }"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
              <span v-if="tab.count" class="tab-count">{{ tab.count }}</span>
            </button>
          </div>

          <div class="feed-content">
            <div v-if="activeTab === 'posts'" class="posts-feed">
              <div v-if="posts.length" class="posts-grid">
                <div v-for="post in posts" :key="post.id" class="post-card">
                  <PostCard :post="post" @like="handleLike" @comment="handleComment" />
                </div>
              </div>
              <div v-else class="empty-state">
                <div class="empty-icon">📝</div>
                <h3>Пока нет постов</h3>
                <p>
                  {{
                    isOwnProfile
                      ? 'Создайте свой первый пост!'
                      : 'Пользователь еще не публиковал посты'
                  }}
                </p>
                <router-link v-if="isOwnProfile" to="/create-post" class="btn btn-primary">
                  Создать пост
                </router-link>
              </div>
            </div>

            <div v-if="activeTab === 'likes'" class="likes-feed">
              <div v-if="likedPosts.length" class="posts-grid">
                <div v-for="post in likedPosts" :key="post.id" class="post-card">
                  <PostCard :post="post" />
                </div>
              </div>
              <div v-else class="empty-state">
                <div class="empty-icon">❤️</div>
                <h3>Пока нет лайков</h3>
                <p>
                  {{
                    isOwnProfile
                      ? 'Лайкайте посты, чтобы они появились здесь'
                      : 'Пользователь еще не ставил лайки'
                  }}
                </p>
              </div>
            </div>

            <div v-if="activeTab === 'media'" class="media-feed">
              <div v-if="media.length" class="media-grid">
                <div
                  v-for="item in media"
                  :key="item.id"
                  class="media-item"
                  @click="openMedia(item)"
                >
                  <img :src="item.url" :alt="item.title" />
                  <div class="media-overlay">
                    <span class="media-type">{{ item.type }}</span>
                    <span class="media-date">{{ formatTime(item.date) }}</span>
                  </div>
                </div>
              </div>
              <div v-else class="empty-state">
                <div class="empty-icon">🖼️</div>
                <h3>Пока нет медиа</h3>
                <p>
                  {{
                    isOwnProfile
                      ? 'Добавляйте фото и видео к постам'
                      : 'Пользователь еще не добавлял медиа'
                  }}
                </p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>

    <EditProfileModal
      v-if="showEditModal"
      :user="user"
      @close="showEditModal = false"
      @updated="handleProfileUpdate"
    />
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import PostCard from '@/components/PostCard.vue'
import EditProfileModal from '@/components/EditProfileModal.vue'

export default {
  name: 'ProfileView',
  components: {
    PostCard,
    EditProfileModal,
  },
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  data() {
    return {
      loading: true,
      user: {},
      posts: [],
      likedPosts: [],
      media: [],
      stats: {},
      gameStats: [],
      activeTab: 'posts',
      showEditModal: false,
      tabs: [
        { id: 'posts', label: 'Посты', count: 0 },
        { id: 'likes', label: 'Лайки', count: 0 },
        { id: 'media', label: 'Медиа', count: 0 },
        { id: 'friends', label: 'Друзья', count: 0 },
      ],
      defaultAvatar: new URL('@/assets/images/Avatar.jpg', import.meta.url).href,
      isFollowing: false,
    }
  },
  computed: {
    isOwnProfile() {
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}')
      return currentUser.id === this.user.id
    },
  },
  async mounted() {
    await this.loadProfile()
  },
  methods: {
    async loadProfile() {
      this.loading = true
      try {
        const userId = this.$route.params.id || JSON.parse(localStorage.getItem('user') || '{}').id
        const response = await fetch(`/api/users/${userId}`)
        const data = await response.json()

        if (data.success) {
          this.user = data.user
          await this.loadUserData()
        }
      } catch (error) {
        console.error('Error loading profile:', error)
      } finally {
        this.loading = false
      }
    },

    async loadUserData() {
      try {
        const postsResponse = await fetch(`/api/users/${this.user.id}/posts`)
        const postsData = await postsResponse.json()
        if (postsData.success) {
          this.posts = postsData.posts
          this.tabs[0].count = postsData.total
        }

        if (this.authStore.isAuthenticated) {
          const statsResponse = await fetch(`/api/users/${this.user.id}/stats`)
          const statsData = await statsResponse.json()
          if (statsData.success) {
            this.stats = statsData.stats
            this.isFollowing = statsData.is_following || false
          }

          const gamesResponse = await fetch('/api/games/scores', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          })
          const gamesData = await gamesResponse.json()
          if (gamesData.success) {
            this.gameStats = gamesData.scores.slice(0, 5)
          }
        }
      } catch (error) {
        console.error('Error loading user data:', error)
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'Неизвестно'
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
      })
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU')
    },

    async toggleFollow() {
      if (!this.authStore.isAuthenticated) {
        this.$router.push('/login')
        return
      }

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch(`/api/friends/${this.user.id}/follow`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        const data = await response.json()
        if (data.success) {
          this.isFollowing = !this.isFollowing
          this.stats.followers += this.isFollowing ? 1 : -1
        }
      } catch (error) {
        console.error('Error toggling follow:', error)
      }
    },

    editCover() {
      console.log('Edit cover')
    },

    editAvatar() {
      console.log('Edit avatar')
    },

    sendMessage() {
      if (!this.authStore.isAuthenticated) {
        this.$router.push('/login')
        return
      }
      this.$router.push(`/messages?to=${this.user.id}`)
    },

    handleLike(postId) {
      console.log('Like post:', postId)
    },

    handleComment(postId) {
      this.$router.push(`/posts/${postId}`)
    },

    openMedia(item) {
      console.log('Open media:', item)
    },

    handleProfileUpdate(updatedUser) {
      this.user = { ...this.user, ...updatedUser }
    },
  },
  watch: {
    '$route.params.id': {
      immediate: true,
      handler() {
        this.loadProfile()
      },
    },
  },
}
</script>

<style scoped>
.profile-view {
  min-height: 100vh;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(138, 43, 226, 0.3);
  border-radius: 50%;
  border-top-color: #8a2be2;
  animation: spin 1s linear infinite;
}

.profile-header {
  position: relative;
  margin-bottom: 2rem;
}

.cover-photo {
  height: 300px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  position: relative;
  overflow: hidden;
}

.cover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.5));
}

.edit-cover-btn {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 20px;
  color: #333;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.edit-cover-btn:hover {
  background: white;
  transform: translateY(-2px);
}

.profile-info {
  display: flex;
  align-items: flex-end;
  position: relative;
  margin-top: -80px;
  padding: 0 2rem;
}

.avatar-section {
  position: relative;
  margin-right: 2rem;
}

.profile-avatar {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  border: 5px solid #1a1a2e;
  object-fit: cover;
  background: #2a2a3e;
}

.edit-avatar-btn {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 40px;
  height: 40px;
  background: #8a2be2;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s;
}

.edit-avatar-btn:hover {
  background: #7a1be2;
  transform: scale(1.1);
}

.profile-details {
  flex: 1;
  padding-bottom: 1rem;
}

.profile-name {
  font-size: 2.5rem;
  color: white;
  margin-bottom: 0.5rem;
}

.profile-bio {
  color: #b0b0b0;
  margin-bottom: 1.5rem;
  max-width: 600px;
  line-height: 1.6;
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
  font-size: 1.8rem;
  font-weight: bold;
  color: white;
  margin-bottom: 0.2rem;
}

.stat-label {
  color: #888;
  font-size: 0.9rem;
}

.profile-actions {
  display: flex;
  gap: 1rem;
}

.btn-action {
  padding: 0.8rem 1.5rem;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
}

.follow-btn {
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  min-width: 120px;
}

.follow-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.message-btn {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid #444;
}

.message-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.edit-btn {
  background: transparent;
  color: #8a2be2;
  border: 2px solid #8a2be2;
}

.edit-btn:hover {
  background: rgba(138, 43, 226, 0.1);
}

.profile-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.profile-sidebar {
  position: sticky;
  top: 100px;
  height: fit-content;
}

.sidebar-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.sidebar-section h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.2rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #333;
}

.info-item {
  margin-bottom: 1rem;
}

.info-label {
  display: block;
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.info-value {
  color: white;
  font-size: 1rem;
}

.genres-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.genre-tag {
  padding: 0.3rem 0.8rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-radius: 15px;
  font-size: 0.85rem;
}

.no-info {
  color: #666;
  font-style: italic;
}

.info-link {
  color: #8a2be2;
  text-decoration: none;
  word-break: break-all;
}

.info-link:hover {
  text-decoration: underline;
}

.game-stats {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.game-stat-item {
  display: flex;
  justify-content: space-between;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
}

.game-name {
  color: white;
  font-size: 0.9rem;
}

.game-score {
  color: #8a2be2;
  font-weight: bold;
}

.playlists-preview {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.playlist-item {
  cursor: pointer;
  transition: transform 0.3s;
}

.playlist-item:hover {
  transform: translateX(5px);
}

.playlist-cover {
  height: 80px;
  border-radius: 10px;
  background-size: cover;
  background-position: center;
  margin-bottom: 0.5rem;
  position: relative;
}

.playlist-count {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  font-size: 0.8rem;
}

.playlist-name {
  color: white;
  font-size: 0.9rem;
  display: block;
  text-align: center;
}

.profile-feed {
  min-height: 100vh;
}

.feed-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #333;
  padding-bottom: 0.5rem;
  overflow-x: auto;
}

.feed-tabs button {
  padding: 0.8rem 1.5rem;
  background: transparent;
  border: none;
  color: #b0b0b0;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  white-space: nowrap;
  position: relative;
  transition: all 0.3s;
}

.feed-tabs button:hover {
  color: white;
}

.feed-tabs button.active {
  color: #8a2be2;
}

.feed-tabs button.active::after {
  content: '';
  position: absolute;
  bottom: -0.6rem;
  left: 0;
  right: 0;
  height: 3px;
  background: #8a2be2;
  border-radius: 3px 3px 0 0;
}

.tab-count {
  margin-left: 0.5rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  font-size: 0.8rem;
}

.feed-content {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
  min-height: 400px;
}

.posts-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.media-item {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  aspect-ratio: 1;
}

.media-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.media-item:hover img {
  transform: scale(1.05);
}

.media-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.media-type {
  background: rgba(138, 43, 226, 0.8);
  padding: 0.2rem 0.5rem;
  border-radius: 5px;
  font-size: 0.8rem;
}

.media-date {
  font-size: 0.8rem;
  opacity: 0.9;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.empty-state p {
  color: #b0b0b0;
  margin-bottom: 2rem;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.btn {
  display: inline-block;
  padding: 0.8rem 2rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1024px) {
  .profile-content {
    grid-template-columns: 1fr;
  }

  .profile-sidebar {
    position: static;
  }
}

@media (max-width: 768px) {
  .profile-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 0 1rem;
  }

  .avatar-section {
    margin-right: 0;
    margin-bottom: 1rem;
  }

  .profile-stats {
    justify-content: center;
    flex-wrap: wrap;
  }

  .profile-actions {
    flex-wrap: wrap;
    justify-content: center;
  }

  .feed-tabs {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .profile-name {
    font-size: 1.8rem;
  }

  .profile-avatar {
    width: 120px;
    height: 120px;
  }

  .feed-tabs {
    flex-direction: column;
  }

  .feed-tabs button {
    text-align: center;
  }
}
</style>
