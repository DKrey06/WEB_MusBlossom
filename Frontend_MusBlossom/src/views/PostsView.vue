<template>
  <div class="posts-view">
    <div class="posts-header">
      <h1>Сообщество музыкантов</h1>
      <p>Читай, общайся и делись музыкой</p>

      <div class="filters-bar">
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск постов, треков, исполнителей..."
            @input="handleSearch"
          />
          <span class="search-icon">🔍</span>
        </div>

        <div class="filter-buttons">
          <button
            v-for="filter in filters"
            :key="filter.id"
            class="filter-btn"
            :class="{ active: activeFilter === filter.id }"
            @click="applyFilter(filter.id)"
          >
            {{ filter.label }}
          </button>
        </div>
      </div>
    </div>

    <div class="posts-content">
      <aside class="sidebar">
        <div class="sidebar-section">
          <h3>Тренды</h3>
          <div class="trending-tags">
            <span class="trend-tag" v-for="tag in trendingTags" :key="tag.name">
              #{{ tag.name }}
              <small>{{ tag.count }}</small>
            </span>
          </div>
        </div>

        <div class="sidebar-section">
          <h3>Популярные авторы</h3>
          <div class="popular-authors">
            <div class="author-card" v-for="author in popularAuthors" :key="author.id">
              <img :src="author.avatar" alt="Avatar" />
              <div class="author-info">
                <strong>{{ author.name }}</strong>
                <span>{{ author.posts }} постов</span>
              </div>
              <button class="follow-btn" @click="followAuthor(author.id)">
                {{ author.isFollowing ? '✓ Подписан' : 'Подписаться' }}
              </button>
            </div>
          </div>
        </div>

        <div class="sidebar-section">
          <h3>Статистика</h3>
          <div class="stats">
            <div class="stat-item">
              <span class="stat-value">{{ stats.totalPosts }}</span>
              <span class="stat-label">Постов</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ stats.activeUsers }}</span>
              <span class="stat-label">Активных</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ stats.dailyPosts }}</span>
              <span class="stat-label">Сегодня</span>
            </div>
          </div>
        </div>
      </aside>

      <main class="posts-feed">
        <div class="create-post-card">
          <div class="create-post-header">
            <img :src="currentUserAvatar" class="user-avatar" alt="Avatar" />
            <input
              type="text"
              placeholder="О чем хочешь рассказать?"
              @click="showCreateModal = true"
            />
          </div>
          <div class="create-post-actions">
            <button class="action-btn" @click="showCreateModal = true">📝 Текст</button>
            <button class="action-btn" @click="showCreateModal = true">🎵 Трек</button>
            <button class="action-btn" @click="showCreateModal = true">🖼️ Фото</button>
            <button class="action-btn" @click="showCreateModal = true">🎥 Видео</button>
          </div>
        </div>

        <div class="posts-list">
          <div v-for="post in filteredPosts" :key="post.id" class="post-item">
            <PostCard :post="post" @like="handleLike" @comment="handleComment" />
          </div>
        </div>

        <div class="pagination">
          <button class="pagination-btn" :disabled="currentPage === 1" @click="prevPage">
            ← Назад
          </button>
          <span class="page-info"> Страница {{ currentPage }} из {{ totalPages }} </span>
          <button class="pagination-btn" :disabled="currentPage === totalPages" @click="nextPage">
            Далее →
          </button>
        </div>
      </main>
    </div>

    <CreatePostModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="handlePostCreated"
    />
  </div>
</template>

<script>
import PostCard from '@/components/PostCard.vue'
import CreatePostModal from '@/components/CreatePostModal.vue'

export default {
  name: 'PostsView',
  components: {
    PostCard,
    CreatePostModal,
  },
  data() {
    return {
      searchQuery: '',
      activeFilter: 'all',
      showCreateModal: false,
      currentPage: 1,
      postsPerPage: 10,
      posts: [],
      filters: [
        { id: 'all', label: 'Все' },
        { id: 'reviews', label: 'Рецензии' },
        { id: 'thoughts', label: 'Мысли' },
        { id: 'quotes', label: 'Цитаты' },
        { id: 'news', label: 'Новости' },
      ],
      trendingTags: [
        { name: 'новинка', count: 245 },
        { name: 'хипхоп', count: 189 },
        { name: 'рок', count: 167 },
        { name: 'обзор', count: 142 },
        { name: 'концерт', count: 128 },
      ],
      popularAuthors: [
        {
          id: 1,
          name: 'Алексей Рокер',
          avatar: 'https://i.pravatar.cc/150?img=12',
          posts: 45,
          isFollowing: false,
        },
        {
          id: 2,
          name: 'Мария Меломана',
          avatar: 'https://i.pravatar.cc/150?img=5',
          posts: 32,
          isFollowing: true,
        },
        {
          id: 3,
          name: 'DJ Петрович',
          avatar: 'https://i.pravatar.cc/150?img=8',
          posts: 28,
          isFollowing: false,
        },
      ],
      stats: {
        totalPosts: 12560,
        activeUsers: 842,
        dailyPosts: 156,
      },
    }
  },
  computed: {
    currentUserAvatar() {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      return user.avatar || 'https://i.pravatar.cc/150?img=1'
    },
    filteredPosts() {
      let filtered = this.posts

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(
          (post) =>
            post.title.toLowerCase().includes(query) ||
            post.content.toLowerCase().includes(query) ||
            post.author.name.toLowerCase().includes(query),
        )
      }

      if (this.activeFilter !== 'all') {
        filtered = filtered.filter((post) => post.type === this.activeFilter)
      }

      const start = (this.currentPage - 1) * this.postsPerPage
      const end = start + this.postsPerPage
      return filtered.slice(start, end)
    },
    totalPages() {
      return Math.ceil(this.posts.length / this.postsPerPage)
    },
  },
  async mounted() {
    await this.loadPosts()
  },
  methods: {
    async loadPosts() {
      try {
        const response = await fetch('/api/posts')
        const data = await response.json()
        if (data.success) {
          this.posts = data.posts
        }
      } catch (error) {
        console.error('Ошибка загрузки постов:', error)
      }
    },
    handleSearch() {
      this.currentPage = 1
    },
    applyFilter(filterId) {
      this.activeFilter = filterId
      this.currentPage = 1
    },
    followAuthor(authorId) {
      const author = this.popularAuthors.find((a) => a.id === authorId)
      if (author) {
        author.isFollowing = !author.isFollowing
      }
    },
    handleLike(postId) {
      console.log('Лайк поста:', postId)
    },
    handleComment(postId) {
      this.$router.push(`/post/${postId}`)
    },
    handlePostCreated(newPost) {
      this.posts.unshift(newPost)
      this.showCreateModal = false
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        window.scrollTo(0, 0)
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        window.scrollTo(0, 0)
      }
    },
  },
}
</script>

<style scoped>
.posts-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.posts-header {
  margin-bottom: 2rem;
}

.posts-header h1 {
  font-size: 2.5rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.posts-header p {
  color: #b0b0b0;
  margin-bottom: 1.5rem;
}

.filters-bar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-box {
  position: relative;
  max-width: 600px;
}

.search-box input {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 3rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s;
}

.search-box input:focus {
  outline: none;
  border-color: #8a2be2;
  background: rgba(255, 255, 255, 0.12);
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

.filter-btn {
  padding: 0.5rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 20px;
  color: #b0b0b0;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.filter-btn:hover {
  background: rgba(138, 43, 226, 0.1);
  border-color: #8a2be2;
  color: #8a2be2;
}

.filter-btn.active {
  background: rgba(138, 43, 226, 0.2);
  border-color: #8a2be2;
  color: #8a2be2;
}

.posts-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
}

.sidebar {
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
}

.trending-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.trend-tag {
  padding: 0.3rem 0.8rem;
  background: rgba(138, 43, 226, 0.2);
  border-radius: 15px;
  color: #8a2be2;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.trend-tag small {
  color: #888;
  font-size: 0.8rem;
}

.popular-authors {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.author-card {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem;
  border-radius: 10px;
  transition: background 0.3s;
}

.author-card:hover {
  background: rgba(255, 255, 255, 0.08);
}

.author-card img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.author-info {
  flex: 1;
}

.author-info strong {
  display: block;
  color: white;
  font-size: 0.9rem;
}

.author-info span {
  color: #888;
  font-size: 0.8rem;
}

.follow-btn {
  padding: 0.3rem 0.8rem;
  background: rgba(138, 43, 226, 0.1);
  border: 1px solid #8a2be2;
  color: #8a2be2;
  border-radius: 15px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.follow-btn:hover {
  background: rgba(138, 43, 226, 0.2);
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
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
  margin-bottom: 0.2rem;
}

.stat-label {
  color: #888;
  font-size: 0.9rem;
}

.posts-feed {
  min-height: 100vh;
}

.create-post-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.create-post-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.create-post-header input {
  flex: 1;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

.create-post-header input:hover {
  background: rgba(255, 255, 255, 0.12);
}

.create-post-actions {
  display: flex;
  gap: 1rem;
}

.action-btn {
  flex: 1;
  padding: 0.8rem;
  background: transparent;
  border: 1px solid #444;
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background: rgba(138, 43, 226, 0.1);
  border-color: #8a2be2;
  color: #8a2be2;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin: 3rem 0;
}

.pagination-btn {
  padding: 0.8rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  background: rgba(138, 43, 226, 0.1);
  border-color: #8a2be2;
  color: #8a2be2;
}

.pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  color: #888;
  font-size: 0.9rem;
}

@media (max-width: 1024px) {
  .posts-content {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .create-post-actions {
    flex-wrap: wrap;
  }

  .action-btn {
    flex: none;
    width: calc(50% - 0.5rem);
  }
}

@media (max-width: 480px) {
  .filter-buttons {
    justify-content: center;
  }

  .action-btn {
    width: 100%;
  }
}
</style>
