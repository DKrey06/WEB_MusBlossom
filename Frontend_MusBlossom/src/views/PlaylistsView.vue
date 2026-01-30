<template>
  <div class="playlists-view">
    <div class="playlists-header">
      <h1>Плейлисты</h1>
      <p>Откройте для себя музыкальные коллекции сообщества</p>
    </div>

    <div class="playlists-controls">
      <div class="controls-top">
        <div class="search-filter">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск плейлистов..."
            @input="searchPlaylists"
          />
          <button class="filter-btn" @click="toggleFilters">Фильтры</button>
        </div>

        <router-link v-if="isAuthenticated" to="/create-playlist" class="create-btn">
          Создать плейлист
        </router-link>
      </div>

      <div v-if="showFilters" class="filters-panel">
        <div class="filter-group">
          <label>Сортировка:</label>
          <select v-model="sortBy">
            <option value="newest">Сначала новые</option>
            <option value="popular">По популярности</option>
            <option value="tracks">По количеству треков</option>
            <option value="alphabetical">По алфавиту</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Жанры:</label>
          <div class="genres-selector">
            <span
              v-for="genre in availableGenres"
              :key="genre"
              :class="{ selected: selectedGenres.includes(genre) }"
              @click="toggleGenre(genre)"
              class="genre-tag"
            >
              {{ genre }}
            </span>
          </div>
        </div>

        <div class="filter-group">
          <label>Длина:</label>
          <div class="range-slider">
            <input type="range" v-model="trackCount" min="1" max="100" @change="applyFilters" />
            <span>{{ trackCount }}+ треков</span>
          </div>
        </div>

        <div class="filter-actions">
          <button class="btn btn-secondary" @click="resetFilters">Сбросить</button>
          <button class="btn btn-primary" @click="applyFilters">Применить</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка плейлистов...</p>
    </div>

    <div v-else class="playlists-content">
      <div class="content-header">
        <h2>
          Все плейлисты <span class="count">({{ filteredPlaylists.length }})</span>
        </h2>
        <div class="view-options">
          <button :class="{ active: viewMode === 'grid' }" @click="viewMode = 'grid'">Сетка</button>
          <button :class="{ active: viewMode === 'list' }" @click="viewMode = 'list'">
            Список
          </button>
        </div>
      </div>

      <div v-if="filteredPlaylists.length" :class="['playlists-container', viewMode]">
        <div
          v-for="playlist in filteredPlaylists"
          :key="playlist.id"
          class="playlist-card"
          @click="$router.push(`/playlists/${playlist.id}`)"
        >
          <div class="playlist-cover">
            <img :src="playlist.cover_url || defaultCover" :alt="playlist.name" />
            <div class="playlist-overlay">
              <span class="track-count">{{ playlist.tracks_count || 0 }} треков</span>
              <span class="play-count">{{ playlist.plays_count || 0 }} прослушиваний</span>
            </div>
          </div>

          <div class="playlist-info">
            <h3>{{ playlist.name }}</h3>
            <p class="playlist-description">{{ playlist.description || 'Без описания' }}</p>

            <div class="playlist-meta">
              <div class="creator-info">
                <img
                  :src="playlist.creator.avatar || defaultAvatar"
                  :alt="playlist.creator.username"
                />
                <span>{{ playlist.creator.username }}</span>
              </div>
              <span class="playlist-date">{{ formatDate(playlist.created_at) }}</span>
            </div>

            <div class="playlist-actions">
              <button class="action-btn" @click.stop="playPlaylist(playlist)">Воспроизвести</button>
              <button class="action-btn" @click.stop="savePlaylist(playlist)">Сохранить</button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="no-playlists">
        <div class="empty-icon">🎧</div>
        <h3>Плейлисты не найдены</h3>
        <p>Попробуйте изменить фильтры поиска</p>
        <button class="btn btn-secondary" @click="resetFilters">Сбросить фильтры</button>
      </div>

      <div v-if="filteredPlaylists.length > 0" class="pagination">
        <button :disabled="currentPage === 1" @click="prevPage" class="pagination-btn">
          ← Назад
        </button>
        <span class="page-info"> Страница {{ currentPage }} из {{ totalPages }} </span>
        <button :disabled="currentPage === totalPages" @click="nextPage" class="pagination-btn">
          Вперед →
        </button>
      </div>
    </div>

    <div class="featured-playlists" v-if="featuredPlaylists.length">
      <h2>Рекомендуемые плейлисты</h2>
      <div class="featured-slider">
        <div
          v-for="playlist in featuredPlaylists"
          :key="playlist.id"
          class="featured-card"
          :style="{
            backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url(${playlist.cover_url || defaultCover})`,
          }"
          @click="$router.push(`/playlists/${playlist.id}`)"
        >
          <div class="featured-content">
            <h3>{{ playlist.name }}</h3>
            <p class="featured-description">{{ playlist.description }}</p>
            <div class="featured-stats">
              <span>{{ playlist.tracks_count }} треков</span>
              <span>{{ playlist.plays_count }} прослушиваний</span>
            </div>
            <button class="btn btn-primary">Слушать</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlaylistsView',
  data() {
    return {
      loading: true,
      playlists: [],
      featuredPlaylists: [],
      searchQuery: '',
      showFilters: false,
      sortBy: 'newest',
      selectedGenres: [],
      trackCount: 1,
      viewMode: 'grid',
      currentPage: 1,
      itemsPerPage: 12,
      availableGenres: [
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
      ],
      defaultCover:
        'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=400&fit=crop',
      defaultAvatar: 'https://i.pravatar.cc/150',
      isAuthenticated: localStorage.getItem('access_token') !== null,
    }
  },
  computed: {
    filteredPlaylists() {
      let filtered = [...this.playlists]

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(
          (p) =>
            p.name.toLowerCase().includes(query) ||
            (p.description && p.description.toLowerCase().includes(query)),
        )
      }

      switch (this.sortBy) {
        case 'newest':
          filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          break
        case 'popular':
          filtered.sort((a, b) => (b.plays_count || 0) - (a.plays_count || 0))
          break
        case 'tracks':
          filtered.sort((a, b) => (b.tracks_count || 0) - (a.tracks_count || 0))
          break
        case 'alphabetical':
          filtered.sort((a, b) => a.name.localeCompare(b.name))
          break
      }

      filtered = filtered.filter((p) => (p.tracks_count || 0) >= this.trackCount)

      return filtered
    },

    paginatedPlaylists() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredPlaylists.slice(start, end)
    },

    totalPages() {
      return Math.ceil(this.filteredPlaylists.length / this.itemsPerPage)
    },
  },
  async mounted() {
    await this.loadPlaylists()
  },
  methods: {
    async loadPlaylists() {
      this.loading = true
      try {
        const response = await fetch('http://localhost:5000/api/playlists')
        const data = await response.json()

        if (data.success) {
          this.playlists = data.playlists
          this.featuredPlaylists = data.playlists.slice(0, 3)
        }
      } catch (error) {
        console.error('Error loading playlists:', error)
        this.playlists = this.getMockPlaylists()
        this.featuredPlaylists = this.playlists.slice(0, 3)
      } finally {
        this.loading = false
      }
    },

    getMockPlaylists() {
      return [
        {
          id: 1,
          name: 'Лучшие хиты 2023',
          description: 'Самые популярные треки этого года',
          cover_url:
            'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=400&fit=crop',
          tracks_count: 25,
          plays_count: 1245,
          created_at: '2023-10-15T10:30:00',
          creator: {
            username: 'musiclover',
            avatar: 'https://i.pravatar.cc/150?img=1',
          },
        },
        {
          id: 2,
          name: 'Рок классика',
          description: 'Вечная классика рок-музыки',
          cover_url:
            'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=800&h=400&fit=crop',
          tracks_count: 30,
          plays_count: 895,
          created_at: '2023-10-10T14:20:00',
          creator: {
            username: 'rockfan',
            avatar: 'https://i.pravatar.cc/150?img=2',
          },
        },
      ]
    },

    searchPlaylists() {
      clearTimeout(this.searchTimer)
      this.searchTimer = setTimeout(() => {
        this.currentPage = 1
      }, 300)
    },

    toggleFilters() {
      this.showFilters = !this.showFilters
    },

    toggleGenre(genre) {
      const index = this.selectedGenres.indexOf(genre)
      if (index === -1) {
        this.selectedGenres.push(genre)
      } else {
        this.selectedGenres.splice(index, 1)
      }
    },

    applyFilters() {
      this.currentPage = 1
      this.showFilters = false
    },

    resetFilters() {
      this.searchQuery = ''
      this.sortBy = 'newest'
      this.selectedGenres = []
      this.trackCount = 1
      this.currentPage = 1
      this.showFilters = false
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
      })
    },

    playPlaylist(playlist) {
      console.log('Playing playlist:', playlist.name)
    },

    savePlaylist(playlist) {
      const saved = JSON.parse(localStorage.getItem('saved_playlists') || '[]')
      if (!saved.find((p) => p.id === playlist.id)) {
        saved.push(playlist)
        localStorage.setItem('saved_playlists', JSON.stringify(saved))
        alert('Плейлист сохранен')
      } else {
        alert('Плейлист уже сохранен')
      }
    },

    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },
  },
}
</script>

<style scoped>
.playlists-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.playlists-header {
  text-align: center;
  margin: 2rem 0 3rem;
}

.playlists-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: white;
}

.playlists-header p {
  color: #b0b0b0;
  font-size: 1.2rem;
}

.playlists-controls {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.controls-top {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.search-filter {
  flex: 1;
  display: flex;
  gap: 1rem;
}

.search-filter input {
  flex: 1;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
}

.filter-btn {
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  font-size: 1rem;
  white-space: nowrap;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.create-btn {
  padding: 1rem 2rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  border: none;
  border-radius: 10px;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s;
  white-space: nowrap;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.filters-panel {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1.5rem;
  margin-top: 1rem;
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

.genres-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.genre-tag {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 20px;
  color: #b0b0b0;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.genre-tag:hover {
  background: rgba(255, 255, 255, 0.1);
}

.genre-tag.selected {
  background: rgba(138, 43, 226, 0.2);
  border-color: #8a2be2;
  color: #8a2be2;
}

.range-slider {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.range-slider input {
  flex: 1;
}

.range-slider span {
  color: white;
  min-width: 80px;
  text-align: right;
}

.filter-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #333;
}

.btn {
  padding: 0.8rem 1.5rem;
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

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
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

.playlists-content {
  margin-bottom: 4rem;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.content-header h2 {
  color: white;
  font-size: 1.8rem;
}

.count {
  color: #8a2be2;
}

.view-options {
  display: flex;
  gap: 0.5rem;
}

.view-options button {
  padding: 0.5rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 5px;
  color: #b0b0b0;
  cursor: pointer;
}

.view-options button.active {
  background: rgba(138, 43, 226, 0.2);
  border-color: #8a2be2;
  color: #8a2be2;
}

.playlists-container.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.playlists-container.list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.playlist-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.playlists-container.grid .playlist-card {
  height: 100%;
}

.playlists-container.list .playlist-card {
  display: flex;
}

.playlist-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
}

.playlist-cover {
  position: relative;
}

.playlists-container.grid .playlist-cover {
  height: 200px;
}

.playlists-container.list .playlist-cover {
  width: 200px;
  height: 200px;
  flex-shrink: 0;
}

.playlist-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.playlist-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  color: white;
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

.playlist-info {
  padding: 1.5rem;
  flex: 1;
}

.playlist-info h3 {
  color: white;
  margin-bottom: 0.8rem;
  font-size: 1.3rem;
}

.playlist-description {
  color: #b0b0b0;
  margin-bottom: 1.5rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.playlist-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
}

.creator-info {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.creator-info img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}

.creator-info span {
  color: white;
  font-size: 0.95rem;
}

.playlist-date {
  color: #888;
  font-size: 0.9rem;
}

.playlist-actions {
  display: flex;
  gap: 1rem;
}

.action-btn {
  flex: 1;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.no-playlists {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.no-playlists h3 {
  color: white;
  margin-bottom: 0.8rem;
  font-size: 1.8rem;
}

.no-playlists p {
  color: #b0b0b0;
  margin-bottom: 2rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #333;
}

.pagination-btn {
  padding: 0.8rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
}

.pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  color: #b0b0b0;
  font-weight: 500;
}

.featured-playlists {
  margin-top: 4rem;
  padding-top: 3rem;
  border-top: 1px solid #333;
}

.featured-playlists h2 {
  color: white;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.featured-slider {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.featured-card {
  background-size: cover;
  background-position: center;
  border-radius: 15px;
  padding: 2rem;
  min-height: 250px;
  display: flex;
  align-items: flex-end;
  cursor: pointer;
  transition: transform 0.3s;
}

.featured-card:hover {
  transform: translateY(-5px);
}

.featured-content {
  width: 100%;
}

.featured-content h3 {
  color: white;
  font-size: 1.8rem;
  margin-bottom: 0.8rem;
}

.featured-description {
  color: #b0b0b0;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.featured-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  color: white;
  font-weight: 500;
}

@media (max-width: 768px) {
  .controls-top {
    flex-direction: column;
  }

  .playlists-container.list .playlist-card {
    flex-direction: column;
  }

  .playlists-container.list .playlist-cover {
    width: 100%;
    height: 200px;
  }

  .featured-slider {
    grid-template-columns: 1fr;
  }

  .pagination {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
