<template>
  <div class="home-view">
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Добро пожаловать в MusBlossom</h1>
        <p class="hero-subtitle">Музыкальная социальная платформа для настоящих меломанов</p>
        <div class="hero-actions">
          <router-link to="/posts" class="btn btn-primary">Исследовать</router-link>
          <router-link to="/register" class="btn btn-secondary">Присоединиться</router-link>
        </div>
      </div>
      <div class="hero-visual">
        <img src="@/assets/images/CATSOUND.jpg" alt="Музыкальная платформа" />
      </div>
    </section>

    <section class="trending-section">
      <div class="section-header">
        <h2>🔥 Популярное сейчас</h2>
        <router-link to="/trending" class="see-all">Смотреть все</router-link>
      </div>

      <div class="trending-grid">
        <div class="trending-card" v-for="item in trendingItems" :key="item.id">
          <div class="trending-image" :style="{ backgroundImage: `url(${item.image})` }">
            <div class="trending-badge">{{ item.type }}</div>
          </div>
          <div class="trending-content">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
            <div class="trending-stats">
              <span class="stat">🎵 {{ item.tracks }} треков</span>
              <span class="stat">❤️ {{ item.likes }} лайков</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="posts-section">
      <div class="section-header">
        <h2>📝 Последние посты</h2>
        <router-link to="/posts" class="see-all">Смотреть все</router-link>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Загрузка постов...</p>
      </div>

      <div v-else-if="error" class="error-message">
        <p>⚠️ {{ error }}</p>
        <button @click="loadRecentPosts" class="btn btn-primary">Повторить</button>
      </div>

      <div v-else-if="recentPosts.length === 0" class="no-posts">
        <p>Пока нет постов. Будьте первым!</p>
        <router-link to="/create-post" class="btn btn-primary">Создать пост</router-link>
      </div>

      <div v-else class="posts-list">
        <div class="post-card" v-for="post in recentPosts" :key="post.id">
          <div class="post-header">
            <img :src="post.author?.avatar || defaultAvatar" class="author-avatar" alt="Avatar" />
            <div class="post-meta">
              <span class="author-name">{{ post.author?.username || 'Пользователь' }}</span>
              <span class="post-time">{{ formatTimeAgo(post.created_at) }}</span>
            </div>
          </div>
          <div class="post-content">
            <h3>{{ post.title || 'Без названия' }}</h3>
            <p>{{ post.content ? post.content.substring(0, 200) + '...' : 'Нет содержания' }}</p>
            <div v-if="post.tags && post.tags.length" class="post-tags">
              <span class="tag" v-for="tag in post.tags" :key="tag">#{{ tag }}</span>
            </div>
          </div>
          <div class="post-actions">
            <button class="action-btn like-btn" @click="likePost(post.id)">
              ❤️ {{ post.likes_count || 0 }}
            </button>
            <button class="action-btn comment-btn" @click="goToPost(post.id)">
              💬 {{ post.comments_count || 0 }}
            </button>
            <button class="action-btn share-btn">↪️ Поделиться</button>
          </div>
        </div>
      </div>
    </section>

    <section class="concerts-section">
      <div class="section-header">
        <h2>🎤 Предстоящие концерты</h2>
        <router-link to="/concerts" class="see-all">Смотреть все</router-link>
      </div>

      <div class="concerts-slider">
        <div class="concert-card" v-for="concert in upcomingConcerts" :key="concert.id">
          <div class="concert-image" :style="{ backgroundImage: `url(${concert.image})` }">
            <div class="concert-date">{{ concert.date }}</div>
          </div>
          <div class="concert-info">
            <h3>{{ concert.artist }}</h3>
            <p class="concert-location">{{ concert.location }}</p>
            <p class="concert-venue">{{ concert.venue }}</p>
            <button class="btn btn-ticket" @click="buyTickets(concert)">Купить билеты</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
})

export default {
  name: 'HomeView',
  data() {
    return {
      trendingItems: [
        {
          id: 1,
          title: 'Лучшие хиты 2024',
          description: 'Топ 50 треков этого года',
          type: 'Плейлист',
          tracks: 50,
          likes: 2345,
          image:
            'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=400&fit=crop',
        },
        {
          id: 2,
          title: 'Русский рок',
          description: 'Классика и современность',
          type: 'Подборка',
          tracks: 25,
          likes: 1890,
          image:
            'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400&h=400&fit=crop',
        },
        {
          id: 3,
          title: 'Lo-Fi для работы',
          description: 'Расслабляющие биты',
          type: 'Плейлист',
          tracks: 30,
          likes: 3120,
          image:
            'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&h=400&fit=crop',
        },
      ],
      recentPosts: [],
      upcomingConcerts: [
        {
          id: 1,
          artist: 'Miyagi & Andy Panda',
          date: '15 дек',
          location: 'Москва',
          venue: 'VTB Арена',
          image:
            'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&h=300&fit=crop',
        },
        {
          id: 2,
          artist: 'Morgenshtern',
          date: '20 дек',
          location: 'Санкт-Петербург',
          venue: 'Сибур Арена',
          image:
            'https://images.unsplash.com/photo-1501281667305-0d4ebd5b1e35?w=600&h=300&fit=crop',
        },
        {
          id: 3,
          artist: 'The Weeknd',
          date: '25 дек',
          location: 'Москва',
          venue: 'Лужники',
          image:
            'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=600&h=300&fit=crop',
        },
      ],
      loading: false,
      error: null,
      defaultAvatar: 'https://i.pravatar.cc/150?img=1',
    }
  },
  async mounted() {
    await this.loadRecentPosts()
  },
  methods: {
    async loadRecentPosts() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/posts', {
          params: {
            per_page: 3,
            page: 1,
          },
        })

        console.log('API Response:', response.data)

        if (response.data.success) {
          this.recentPosts = response.data.posts || []
          console.log('Загружено постов:', this.recentPosts.length)
        } else {
          this.error = 'Ошибка загрузки постов: ' + (response.data.error || 'Неизвестная ошибка')
          console.error('Ошибка загрузки постов:', response.data.error)
        }
      } catch (error) {
        console.error('Ошибка при загрузке постов:', error)

        if (error.response) {
          if (error.response.status === 404) {
            this.error = 'API endpoint не найден'
          } else if (error.response.status === 500) {
            this.error = 'Ошибка на сервере'
          } else {
            this.error = `Ошибка сервера: ${error.response.status}`
          }
          console.error('Response data:', error.response.data)
        } else if (error.request) {
          this.error = 'Не удается подключиться к серверу. Проверьте запущен ли бэкенд.'
          console.error('Request error:', error.request)
        } else {
          this.error = 'Ошибка при выполнении запроса: ' + error.message
        }
      } finally {
        this.loading = false
      }
    },

    formatTimeAgo(dateString) {
      if (!dateString) return ''

      const date = new Date(dateString)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMs / 3600000)
      const diffDays = Math.floor(diffMs / 86400000)

      if (diffMins < 60) {
        return `${diffMins} мин назад`
      } else if (diffHours < 24) {
        return `${diffHours} ч назад`
      } else if (diffDays < 7) {
        return `${diffDays} д назад`
      } else {
        return date.toLocaleDateString('ru-RU')
      }
    },

    async likePost(postId) {
      try {
        const response = await api.post(`/posts/${postId}/like`, null, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        })

        if (response.data.success) {
          const post = this.recentPosts.find((p) => p.id === postId)
          if (post) {
            post.likes_count = response.data.likes_count
          }
        }
      } catch (error) {
        console.error('Ошибка при лайке поста:', error)
        if (error.response?.status === 401) {
          alert('Для лайка нужно войти в систему')
        }
      }
    },

    goToPost(postId) {
      this.$router.push(`/posts/${postId}`)
    },

    buyTickets(concert) {
      console.log('Покупка билетов на:', concert.artist)
      alert(`Покупка билетов на ${concert.artist} - функция в разработке`)
    },
  },
}
</script>

<style scoped>
.error-message {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 0, 0, 0.1);
  border-radius: 15px;
  border: 1px solid rgba(255, 0, 0, 0.3);
}

.error-message p {
  color: #ff6b6b;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  margin: 3rem 0;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.1), rgba(75, 0, 130, 0.1));
  border-radius: 20px;
}

.hero-title {
  font-size: 2.5rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #b0b0b0;
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.8rem 2rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
  border: none;
  cursor: pointer;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
}

.btn-secondary {
  background: transparent;
  border: 2px solid #8a2be2;
  color: #8a2be2;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.btn-secondary:hover {
  background: rgba(138, 43, 226, 0.1);
}

.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}

.hero-visual img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 3rem 0 1.5rem;
}

.section-header h2 {
  font-size: 2rem;
  color: white;
}

.see-all {
  color: #8a2be2;
  text-decoration: none;
  font-weight: 500;
}

.see-all:hover {
  text-decoration: underline;
}

/* Тренды */
.trending-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.trending-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  overflow: hidden;
  transition: transform 0.3s;
}

.trending-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
}

.trending-image {
  height: 200px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.trending-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: #8a2be2;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
}

.trending-content {
  padding: 1.5rem;
}

.trending-content h3 {
  margin-bottom: 0.5rem;
  color: white;
  font-size: 1.3rem;
}

.trending-content p {
  color: #b0b0b0;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.trending-stats {
  display: flex;
  gap: 1rem;
  color: #888;
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

.no-posts {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 15px;
}

.no-posts p {
  color: #b0b0b0;
  margin-bottom: 1rem;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  transition: background 0.3s;
}

.post-card:hover {
  background: rgba(255, 255, 255, 0.08);
}

.post-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.post-meta {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-weight: 600;
  color: white;
  font-size: 1rem;
}

.post-time {
  font-size: 0.9rem;
  color: #888;
}

.post-content h3 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.post-content p {
  color: #b0b0b0;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  line-height: 1.5;
}

.post-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  padding: 0.2rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
}

.post-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.action-btn {
  background: transparent;
  border: 1px solid #444;
  color: #b0b0b0;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.action-btn:hover {
  background: rgba(138, 43, 226, 0.1);
  border-color: #8a2be2;
  color: #8a2be2;
}

.concerts-slider {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.concert-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  overflow: hidden;
  transition: transform 0.3s;
}

.concert-card:hover {
  transform: translateY(-5px);
}

.concert-image {
  height: 200px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.concert-date {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #8a2be2;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  font-weight: 600;
}

.concert-info {
  padding: 1.5rem;
}

.concert-info h3 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.3rem;
}

.concert-location {
  color: #8a2be2;
  font-weight: 500;
  margin-bottom: 0.2rem;
}

.concert-venue {
  color: #b0b0b0;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.btn-ticket {
  width: 100%;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  border: none;
  padding: 0.8rem;
  border-radius: 10px;
  cursor: pointer;
  transition: opacity 0.3s;
  font-weight: 600;
}

.btn-ticket:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 2rem;
    padding: 1.5rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .hero-actions {
    justify-content: center;
    flex-wrap: wrap;
  }

  .hero-visual {
    height: 250px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    margin: 2rem 0 1rem;
  }

  .section-header h2 {
    font-size: 1.5rem;
  }

  .concerts-slider,
  .trending-grid {
    grid-template-columns: 1fr;
  }

  .btn {
    padding: 0.7rem 1.5rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .hero-visual {
    height: 200px;
  }

  .hero-title {
    font-size: 1.8rem;
  }

  .trending-content h3,
  .post-content h3,
  .concert-info h3 {
    font-size: 1.1rem;
  }

  .post-actions {
    flex-wrap: wrap;
  }

  .action-btn {
    flex: 1;
    min-width: 80px;
    text-align: center;
  }
}
</style>
