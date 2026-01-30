<template>
  <div class="search-view">
    <div class="search-header">
      <div class="search-box-large">
        <input
          type="text"
          v-model="query"
          placeholder="Поиск музыки, исполнителей, постов, пользователей..."
          @keyup.enter="performSearch"
          ref="searchInput"
        />
        <button class="search-btn" @click="performSearch">
          <span>Поиск</span>
        </button>
      </div>
    </div>

    <div class="search-container">
      <div class="search-filters">
        <div class="filter-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="{ active: activeTab === tab.id }"
            @click="changeTab(tab.id)"
          >
            {{ tab.label }}
            <span class="tab-count" v-if="getCount(tab.id) > 0">
              {{ getCount(tab.id) }}
            </span>
          </button>
        </div>

        <div class="advanced-filters" v-if="showAdvanced">
          <div class="filter-group">
            <label>Сортировать по:</label>
            <select v-model="sortBy">
              <option value="relevance">Релевантности</option>
              <option value="popularity">Популярности</option>
              <option value="newest">Сначала новые</option>
              <option value="oldest">Сначала старые</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Период:</label>
            <select v-model="timeRange">
              <option value="all">За все время</option>
              <option value="day">За день</option>
              <option value="week">За неделю</option>
              <option value="month">За месяц</option>
              <option value="year">За год</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Тип контента:</label>
            <div class="checkbox-group">
              <label>
                <input type="checkbox" v-model="filters.contentTypes.posts" />
                <span>Посты</span>
              </label>
              <label>
                <input type="checkbox" v-model="filters.contentTypes.users" />
                <span>Пользователи</span>
              </label>
              <label>
                <input type="checkbox" v-model="filters.contentTypes.playlists" />
                <span>Плейлисты</span>
              </label>
              <label>
                <input type="checkbox" v-model="filters.contentTypes.tracks" />
                <span>Треки</span>
              </label>
            </div>
          </div>
        </div>

        <button class="toggle-filters" @click="showAdvanced = !showAdvanced">
          {{ showAdvanced ? 'Скрыть фильтры' : 'Расширенные фильтры' }}
        </button>
      </div>

      <div class="search-results">
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Идет поиск...</p>
        </div>

        <div v-else-if="hasResults" class="results-content">
          <div v-if="activeTab === 'users' && results.users.length" class="results-section">
            <h2>Пользователи</h2>
            <div class="users-grid">
              <div v-for="user in results.users" :key="user.id" class="user-card">
                <router-link :to="`/profile/${user.username}`" class="user-link">
                  <img
                    :src="user.avatar || defaultAvatar"
                    :alt="user.username"
                    class="user-avatar"
                  />
                  <div class="user-info">
                    <h3 class="user-name">{{ user.username }}</h3>
                    <p class="user-bio" v-if="user.bio">{{ user.bio }}</p>
                    <div class="user-stats">
                      <span>{{ user.posts_count }} постов</span>
                      <span>{{ user.followers_count }} подписчиков</span>
                    </div>
                  </div>
                </router-link>
                <button class="follow-btn" v-if="!user.is_following">Подписаться</button>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'posts' && results.posts.length" class="results-section">
            <h2>Посты</h2>
            <div class="posts-list">
              <div v-for="post in results.posts" :key="post.id" class="post-card">
                <div class="post-header">
                  <img
                    :src="post.author.avatar || defaultAvatar"
                    :alt="post.author.username"
                    class="author-avatar"
                  />
                  <div class="post-meta">
                    <span class="author-name">{{ post.author.username }}</span>
                    <span class="post-time">{{ formatTime(post.created_at) }}</span>
                  </div>
                </div>
                <h3 class="post-title">{{ post.title }}</h3>
                <p class="post-content">{{ post.content }}</p>
                <div class="post-stats">
                  <span>{{ post.likes_count }} лайков</span>
                  <span>{{ post.comments_count }} комментариев</span>
                </div>
                <router-link :to="`/posts/${post.id}`" class="read-more"
                  >Читать далее →</router-link
                >
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'playlists' && results.playlists.length" class="results-section">
            <h2>Плейлисты</h2>
            <div class="playlists-grid">
              <div v-for="playlist in results.playlists" :key="playlist.id" class="playlist-card">
                <div class="playlist-cover">
                  <img :src="playlist.cover || defaultPlaylistCover" :alt="playlist.name" />
                  <div class="track-count">{{ playlist.tracks_count }} треков</div>
                </div>
                <div class="playlist-info">
                  <h3>{{ playlist.name }}</h3>
                  <p class="playlist-description">{{ playlist.description }}</p>
                  <div class="playlist-creator">
                    <img
                      :src="playlist.creator.avatar || defaultAvatar"
                      :alt="playlist.creator.username"
                    />
                    <span>{{ playlist.creator.username }}</span>
                  </div>
                  <div class="playlist-stats">
                    <span>{{ playlist.plays_count }} прослушиваний</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'tracks' && results.tracks.length" class="results-section">
            <h2>Треки</h2>
            <div class="tracks-list">
              <div v-for="track in results.tracks" :key="track.id" class="track-card">
                <img
                  :src="track.cover || defaultTrackCover"
                  :alt="track.title"
                  class="track-cover"
                />
                <div class="track-info">
                  <h3>{{ track.title }}</h3>
                  <p class="track-artist">{{ track.artist }}</p>
                  <p class="track-album">{{ track.album }}</p>
                  <div class="track-meta">
                    <span>{{ formatDuration(track.duration) }}</span>
                    <span>{{ track.plays_count }} прослушиваний</span>
                  </div>
                </div>
                <button class="play-btn">Воспроизвести</button>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="query && !loading" class="no-results">
          <div class="no-results-icon">🔍</div>
          <h3>Ничего не найдено</h3>
          <p>Попробуйте изменить запрос или использовать другие ключевые слова</p>
          <div class="suggestions">
            <p>Возможно, вы искали:</p>
            <div class="suggestion-tags">
              <span @click="setSuggestion('The Weeknd')">The Weeknd</span>
              <span @click="setSuggestion('Dua Lipa')">Dua Lipa</span>
              <span @click="setSuggestion('Bohemian Rhapsody')">Bohemian Rhapsody</span>
              <span @click="setSuggestion('Рок музыка')">Рок музыка</span>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <div class="empty-icon">🔍</div>
          <h3>Начните поиск</h3>
          <p>
            Введите запрос в поле выше, чтобы найти музыку, исполнителей, посты или пользователей
          </p>

          <div class="popular-searches">
            <h4>Популярные запросы:</h4>
            <div class="popular-tags">
              <span @click="setSuggestion('Поп')">Поп</span>
              <span @click="setSuggestion('Рок')">Рок</span>
              <span @click="setSuggestion('Хип-хоп')">Хип-хоп</span>
              <span @click="setSuggestion('Джаз')">Джаз</span>
              <span @click="setSuggestion('Классика')">Классика</span>
            </div>
          </div>
        </div>
      </div>

      <div class="search-sidebar" v-if="hasResults">
        <div class="sidebar-section">
          <h3>Связанные теги</h3>
          <div class="tags-cloud">
            <span
              v-for="tag in relatedTags"
              :key="tag"
              @click="addTagToSearch(tag)"
              class="tag"
              :style="{ fontSize: `${getTagSize(tag)}px` }"
            >
              {{ tag }}
            </span>
          </div>
        </div>

        <div class="sidebar-section">
          <h3>История поиска</h3>
          <div class="search-history">
            <div
              v-for="item in searchHistory"
              :key="item.id"
              class="history-item"
              @click="setQuery(item.query)"
            >
              <span>{{ item.query }}</span>
              <small>{{ formatTime(item.date) }}</small>
            </div>
          </div>
          <button class="clear-history" @click="clearHistory">Очистить историю</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchView',
  data() {
    return {
      query: '',
      activeTab: 'all',
      tabs: [
        { id: 'all', label: 'Все' },
        { id: 'users', label: 'Пользователи' },
        { id: 'posts', label: 'Посты' },
        { id: 'playlists', label: 'Плейлисты' },
        { id: 'tracks', label: 'Треки' },
      ],
      showAdvanced: false,
      loading: false,
      sortBy: 'relevance',
      timeRange: 'all',
      filters: {
        contentTypes: {
          posts: true,
          users: true,
          playlists: true,
          tracks: true,
        },
      },
      results: {
        users: [],
        posts: [],
        playlists: [],
        tracks: [],
      },
      searchHistory: [],
      relatedTags: ['Рок', 'Поп', 'Хип-хоп', '2023', 'Новинки', 'Классика', 'Джаз', 'Инди'],
      defaultAvatar: 'https://i.pravatar.cc/150',
      defaultPlaylistCover:
        'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=400&fit=crop',
      defaultTrackCover:
        'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800&h=800&fit=crop',
    }
  },
  computed: {
    hasResults() {
      return Object.values(this.results).some((arr) => arr.length > 0)
    },
    allResults() {
      return [
        ...this.results.users,
        ...this.results.posts,
        ...this.results.playlists,
        ...this.results.tracks,
      ]
    },
  },
  mounted() {
    this.loadSearchHistory()
    const queryParam = this.$route.query.q
    if (queryParam) {
      this.query = queryParam
      this.performSearch()
    }
    this.$refs.searchInput?.focus()
  },
  methods: {
    async performSearch() {
      if (!this.query.trim()) return

      this.loading = true

      try {
        this.saveToHistory()

        const [usersRes, postsRes, playlistsRes] = await Promise.all([
          this.searchUsers(),
          this.searchPosts(),
          this.searchPlaylists(),
        ])

        this.results = {
          users: usersRes,
          posts: postsRes,
          playlists: playlistsRes,
          tracks: this.searchTracks(),
        }

        if (this.activeTab === 'all' && !this.allResults.length) {
          for (const tab of this.tabs.slice(1)) {
            if (this.results[tab.id]?.length) {
              this.activeTab = tab.id
              break
            }
          }
        }
      } catch (error) {
        console.error('Search error:', error)
      } finally {
        this.loading = false
      }
    },

    async searchUsers() {
      try {
        const response = await fetch(
          `http://localhost:5000/api/search?q=${encodeURIComponent(this.query)}`,
        )
        const data = await response.json()
        return data.success ? data.results.users || [] : []
      } catch {
        return this.getMockUsers()
      }
    },

    async searchPosts() {
      try {
        const response = await fetch(
          `http://localhost:5000/api/posts?q=${encodeURIComponent(this.query)}`,
        )
        const data = await response.json()
        return data.success ? data.posts || [] : []
      } catch {
        return this.getMockPosts()
      }
    },

    async searchPlaylists() {
      try {
        const response = await fetch(
          `http://localhost:5000/api/playlists?q=${encodeURIComponent(this.query)}`,
        )
        const data = await response.json()
        return data.success ? data.playlists || [] : []
      } catch {
        return this.getMockPlaylists()
      }
    },

    searchTracks() {
      return [
        {
          id: 1,
          title: 'Blinding Lights',
          artist: 'The Weeknd',
          album: 'After Hours',
          cover:
            'https://i.scdn.co/image/ab67616d00001e02/86a0f12c8d1c65b6e6c8b1a0f2c5e8b1d5b3a8f2',
          duration: 200000,
          plays_count: 2450000,
        },
        {
          id: 2,
          title: 'Levitating',
          artist: 'Dua Lipa',
          album: 'Future Nostalgia',
          cover:
            'https://i.scdn.co/image/ab67616d00001e02/f2b8b5b5f5b5f5b5f5b5f5b5f5b5f5b5f5b5f5b5',
          duration: 203000,
          plays_count: 1980000,
        },
      ]
    },

    getMockUsers() {
      return [
        {
          id: 1,
          username: 'musiclover',
          avatar: 'https://i.pravatar.cc/150?img=1',
          bio: 'Любитель музыки всех жанров',
          posts_count: 42,
          followers_count: 128,
          is_following: false,
        },
        {
          id: 2,
          username: 'rockfan',
          avatar: 'https://i.pravatar.cc/150?img=2',
          bio: 'Рок навсегда!',
          posts_count: 18,
          followers_count: 56,
          is_following: true,
        },
      ]
    },

    getMockPosts() {
      return [
        {
          id: 1,
          title: 'Мои мысли о новом альбоме',
          content: 'Недавно вышел новый альбом, и я хочу поделиться своими впечатлениями...',
          author: {
            username: 'musiclover',
            avatar: 'https://i.pravatar.cc/150?img=1',
          },
          created_at: '2023-10-15T10:30:00',
          likes_count: 24,
          comments_count: 8,
        },
      ]
    },

    getMockPlaylists() {
      return [
        {
          id: 1,
          name: 'Лучшие хиты 2023',
          description: 'Самые популярные треки этого года',
          cover:
            'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=400&fit=crop',
          tracks_count: 25,
          creator: {
            username: 'musiclover',
            avatar: 'https://i.pravatar.cc/150?img=1',
          },
          plays_count: 1245,
        },
      ]
    },

    changeTab(tabId) {
      this.activeTab = tabId
    },

    getCount(tabId) {
      if (tabId === 'all') return this.allResults.length
      return this.results[tabId]?.length || 0
    },

    setSuggestion(suggestion) {
      this.query = suggestion
      this.performSearch()
    },

    setQuery(query) {
      this.query = query
      this.performSearch()
    },

    addTagToSearch(tag) {
      if (!this.query.includes(tag)) {
        this.query = this.query ? `${this.query} ${tag}` : tag
        this.performSearch()
      }
    },

    getTagSize(tag) {
      const baseSize = 14
      const popularity = {
        Рок: 3,
        Поп: 3,
        'Хип-хоп': 2,
        2023: 2,
        Новинки: 1,
        Классика: 1,
        Джаз: 1,
        Инди: 1,
      }
      return baseSize + (popularity[tag] || 0)
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diff = Math.floor((now - date) / (1000 * 60))

      if (diff < 60) return `${diff} мин назад`
      if (diff < 24 * 60) return `${Math.floor(diff / 60)} ч назад`
      return date.toLocaleDateString('ru-RU')
    },

    formatDuration(ms) {
      const minutes = Math.floor(ms / 60000)
      const seconds = ((ms % 60000) / 1000).toFixed(0)
      return `${minutes}:${seconds.padStart(2, '0')}`
    },

    saveToHistory() {
      const historyItem = {
        id: Date.now(),
        query: this.query,
        date: new Date().toISOString(),
      }

      this.searchHistory.unshift(historyItem)
      if (this.searchHistory.length > 10) {
        this.searchHistory = this.searchHistory.slice(0, 10)
      }

      localStorage.setItem('searchHistory', JSON.stringify(this.searchHistory))
    },

    loadSearchHistory() {
      const saved = localStorage.getItem('searchHistory')
      if (saved) {
        this.searchHistory = JSON.parse(saved)
      }
    },

    clearHistory() {
      if (confirm('Очистить историю поиска?')) {
        this.searchHistory = []
        localStorage.removeItem('searchHistory')
      }
    },
  },
}
</script>

<style scoped>
.search-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.search-header {
  padding: 2rem 0 3rem;
}

.search-box-large {
  display: flex;
  gap: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

.search-box-large input {
  flex: 1;
  padding: 1.2rem 1.5rem;
  background: rgba(255, 255, 255, 0.08);
  border: 2px solid #444;
  border-radius: 15px;
  color: white;
  font-size: 1.1rem;
  transition: all 0.3s;
}

.search-box-large input:focus {
  outline: none;
  border-color: #8a2be2;
  box-shadow: 0 0 0 3px rgba(138, 43, 226, 0.1);
}

.search-btn {
  padding: 1.2rem 2.5rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s;
  white-space: nowrap;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.search-container {
  display: grid;
  grid-template-columns: 300px 1fr 300px;
  gap: 2rem;
  min-height: 600px;
}

@media (max-width: 1200px) {
  .search-container {
    grid-template-columns: 250px 1fr;
  }

  .search-sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .search-container {
    grid-template-columns: 1fr;
  }
}

.search-filters {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  height: fit-content;
}

.filter-tabs {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.filter-tabs button {
  padding: 1rem 1.5rem;
  background: transparent;
  border: none;
  color: #b0b0b0;
  text-align: left;
  cursor: pointer;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-tabs button:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.filter-tabs button.active {
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  font-weight: 500;
}

.tab-count {
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  font-size: 0.85rem;
  min-width: 30px;
  text-align: center;
}

.advanced-filters {
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.filter-group {
  margin-bottom: 1.5rem;
}

.filter-group label {
  display: block;
  color: white;
  margin-bottom: 0.8rem;
  font-weight: 500;
}

.filter-group select {
  width: 100%;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  cursor: pointer;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  color: #b0b0b0;
  cursor: pointer;
  font-weight: normal;
}

.checkbox-group input {
  width: 18px;
  height: 18px;
}

.toggle-filters {
  width: 100%;
  padding: 0.8rem;
  background: transparent;
  border: 1px solid #444;
  border-radius: 10px;
  color: #8a2be2;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.toggle-filters:hover {
  background: rgba(138, 43, 226, 0.1);
}

.search-results {
  min-height: 500px;
}

.loading {
  text-align: center;
  padding: 4rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(138, 43, 226, 0.3);
  border-radius: 50%;
  border-top-color: #8a2be2;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.results-section {
  margin-bottom: 3rem;
}

.results-section h2 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #333;
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.user-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.user-link {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  text-decoration: none;
  flex: 1;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  flex: 1;
}

.user-name {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.user-bio {
  color: #b0b0b0;
  margin-bottom: 0.8rem;
  font-size: 0.95rem;
  line-height: 1.4;
}

.user-stats {
  display: flex;
  gap: 1rem;
  color: #888;
  font-size: 0.9rem;
}

.follow-btn {
  padding: 0.5rem 1.5rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border: 1px solid #8a2be2;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
  white-space: nowrap;
}

.follow-btn:hover {
  background: rgba(138, 43, 226, 0.3);
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.post-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  transition: all 0.3s;
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
  flex: 1;
}

.author-name {
  display: block;
  color: white;
  font-weight: 500;
  margin-bottom: 0.2rem;
}

.post-time {
  color: #888;
  font-size: 0.9rem;
}

.post-title {
  color: white;
  margin-bottom: 0.8rem;
  font-size: 1.3rem;
}

.post-content {
  color: #b0b0b0;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  color: #888;
  font-size: 0.9rem;
}

.read-more {
  color: #8a2be2;
  text-decoration: none;
  font-weight: 500;
}

.read-more:hover {
  text-decoration: underline;
}

.playlists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.playlist-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  overflow: hidden;
  transition: all 0.3s;
}

.playlist-card:hover {
  transform: translateY(-3px);
}

.playlist-cover {
  height: 150px;
  position: relative;
}

.playlist-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.track-count {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 10px;
  font-size: 0.85rem;
}

.playlist-info {
  padding: 1.5rem;
}

.playlist-info h3 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.playlist-description {
  color: #b0b0b0;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.playlist-creator {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1rem;
}

.playlist-creator img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}

.playlist-creator span {
  color: #888;
  font-size: 0.9rem;
}

.playlist-stats {
  color: #888;
  font-size: 0.9rem;
}

.tracks-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.track-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  transition: all 0.3s;
}

.track-card:hover {
  background: rgba(255, 255, 255, 0.08);
}

.track-cover {
  width: 60px;
  height: 60px;
  border-radius: 5px;
  object-fit: cover;
}

.track-info {
  flex: 1;
}

.track-info h3 {
  color: white;
  margin-bottom: 0.3rem;
  font-size: 1.1rem;
}

.track-artist {
  color: #8a2be2;
  margin-bottom: 0.2rem;
  font-size: 0.95rem;
}

.track-album {
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.track-meta {
  display: flex;
  gap: 1rem;
  color: #888;
  font-size: 0.9rem;
}

.play-btn {
  padding: 0.5rem 1.5rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border: 1px solid #8a2be2;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.play-btn:hover {
  background: rgba(138, 43, 226, 0.3);
}

.no-results,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.no-results-icon,
.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.no-results h3,
.empty-state h3 {
  color: white;
  margin-bottom: 0.8rem;
  font-size: 1.8rem;
}

.no-results p,
.empty-state p {
  color: #b0b0b0;
  margin-bottom: 2rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
}

.suggestions,
.popular-searches {
  margin-top: 2rem;
}

.suggestions p,
.popular-searches h4 {
  color: white;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.suggestion-tags,
.popular-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  justify-content: center;
}

.suggestion-tags span,
.popular-tags span {
  padding: 0.5rem 1rem;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
}

.suggestion-tags span:hover,
.popular-tags span:hover {
  background: rgba(138, 43, 226, 0.3);
  transform: translateY(-2px);
}

.search-sidebar {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.sidebar-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
}

.sidebar-section h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #333;
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
}

.tag {
  padding: 0.5rem 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  color: #b0b0b0;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.tag:hover {
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
}

.search-history {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-bottom: 1.5rem;
  max-height: 300px;
  overflow-y: auto;
}

.history-item {
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.history-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.history-item span {
  display: block;
  color: white;
  margin-bottom: 0.3rem;
  font-weight: 500;
}

.history-item small {
  color: #888;
  font-size: 0.85rem;
}

.clear-history {
  width: 100%;
  padding: 0.8rem;
  background: transparent;
  border: 1px solid #444;
  border-radius: 10px;
  color: #ff4757;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.clear-history:hover {
  background: rgba(255, 71, 87, 0.1);
  border-color: #ff4757;
}
</style>
