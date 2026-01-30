<template>
  <div class="post-detail-view">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>

    <div v-else-if="post" class="post-container">
      <router-link to="/posts" class="back-link">← Назад к постам</router-link>

      <div class="post-card detailed">
        <div class="post-header">
          <img :src="post.author.avatar" class="author-avatar" alt="Avatar" />
          <div class="post-meta">
            <div class="author-info">
              <span class="author-name">{{ post.author.name }}</span>
              <span class="author-badge" v-if="post.author.isVerified">✓</span>
            </div>
            <span class="post-time">{{ formatDate(post.created_at) }}</span>
          </div>
        </div>

        <div class="post-content">
          <h1 class="post-title">{{ post.title }}</h1>
          <div class="post-type">{{ getPostTypeLabel(post.post_type) }}</div>

          <div class="post-text" v-html="formatContent(post.content)"></div>

          <div v-if="post.track_name" class="track-info">
            <div class="track-icon">🎵</div>
            <div class="track-details">
              <strong>{{ post.track_name }}</strong>
              <span v-if="post.artist_name">by {{ post.artist_name }}</span>
            </div>
          </div>
        </div>

        <div class="post-stats">
          <div class="stat">
            <span class="stat-icon">❤️</span>
            <span class="stat-value">{{ post.likes_count }}</span>
            <span class="stat-label">лайков</span>
          </div>
          <div class="stat">
            <span class="stat-icon">💬</span>
            <span class="stat-value">{{ post.comments_count }}</span>
            <span class="stat-label">комментариев</span>
          </div>
          <div class="stat">
            <span class="stat-icon">👁️</span>
            <span class="stat-value">{{ post.views_count || 0 }}</span>
            <span class="stat-label">просмотров</span>
          </div>
        </div>

        <div class="post-actions">
          <button class="action-btn like-btn" @click="toggleLike">
            {{ post.is_liked ? '❤️' : '🤍' }} {{ post.likes_count }}
          </button>
          <button class="action-btn comment-btn" @click="focusComment">💬 Комментировать</button>
          <button class="action-btn share-btn" @click="sharePost">↪️ Поделиться</button>
          <button class="action-btn save-btn" @click="toggleSave">
            {{ post.is_saved ? '★' : '☆' }}
          </button>
        </div>
      </div>

      <div class="comments-section">
        <h2>Комментарии ({{ comments.length }})</h2>

        <div class="add-comment">
          <img :src="currentUserAvatar" class="comment-user-avatar" alt="Avatar" />
          <div class="comment-input-container">
            <textarea
              v-model="newComment"
              placeholder="Напишите комментарий..."
              @keydown.enter.exact.prevent="addComment"
              rows="3"
            ></textarea>
            <button @click="addComment" class="submit-comment-btn">Отправить</button>
          </div>
        </div>

        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment">
            <img :src="comment.author.avatar" class="comment-avatar" alt="Avatar" />
            <div class="comment-content">
              <div class="comment-header">
                <span class="comment-author">{{ comment.author.name }}</span>
                <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
              </div>
              <p class="comment-text">{{ comment.content }}</p>
              <div class="comment-actions">
                <button class="comment-action-btn" @click="likeComment(comment.id)">
                  ❤️ {{ comment.likes_count || 0 }}
                </button>
                <button class="comment-action-btn" @click="replyToComment(comment)">
                  Ответить
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="similarPosts.length" class="similar-posts">
        <h2>Похожие посты</h2>
        <div class="similar-posts-grid">
          <router-link
            v-for="similar in similarPosts"
            :key="similar.id"
            :to="`/posts/${similar.id}`"
            class="similar-post"
          >
            <h3>{{ similar.title }}</h3>
            <p>{{ similar.content.substring(0, 100) }}...</p>
            <div class="similar-post-meta">
              <span>👤 {{ similar.author.username }}</span>
              <span>❤️ {{ similar.likes_count }}</span>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <div v-else class="not-found">
      <h2>Пост не найден</h2>
      <p>Возможно, он был удален или перемещен.</p>
      <router-link to="/posts" class="btn btn-primary"> Вернуться к постам </router-link>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'PostDetailView',
  props: ['id'],
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },
  data() {
    return {
      post: null,
      comments: [],
      similarPosts: [],
      newComment: '',
      loading: true,
    }
  },
  computed: {
    currentUserAvatar() {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      return user.avatar || 'https://i.pravatar.cc/150?img=1'
    },
  },
  async mounted() {
    await this.loadPost()
  },
  methods: {
    async loadPost() {
      try {
        const response = await fetch(`/api/posts/${this.$route.params.id}`)
        const data = await response.json()

        if (data.success) {
          this.post = data.post
          this.comments = data.comments || []
          await this.loadSimilarPosts()
        }
      } catch (error) {
        console.error('Error loading post:', error)
      } finally {
        this.loading = false
      }
    },

    async loadSimilarPosts() {
      try {
        const response = await fetch(`/api/posts?type=${this.post.post_type}`)
        const data = await response.json()

        if (data.success) {
          this.similarPosts = data.posts.filter((p) => p.id !== this.post.id).slice(0, 3)
        }
      } catch (error) {
        console.error('Error loading similar posts:', error)
      }
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    },

    formatTime(dateString) {
      const date = new Date(dateString)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMs / 3600000)
      const diffDays = Math.floor(diffMs / 86400000)

      if (diffMins < 60) return `${diffMins} мин назад`
      if (diffHours < 24) return `${diffHours} ч назад`
      if (diffDays < 7) return `${diffDays} д назад`
      return date.toLocaleDateString('ru-RU')
    },

    getPostTypeLabel(type) {
      const types = {
        thought: 'Мысли',
        review: 'Рецензия',
        news: 'Новости',
        quote: 'Цитата',
      }
      return types[type] || 'Пост'
    },

    formatContent(content) {
      return content.replace(/\n/g, '<br>')
    },

    async toggleLike() {
      if (!this.authStore.isAuthenticated) {
        this.$router.push('/login')
        return
      }

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch(`/api/posts/${this.post.id}/like`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        const data = await response.json()
        if (data.success) {
          this.post.is_liked = !this.post.is_liked
          this.post.likes_count = data.likes_count
        }
      } catch (error) {
        console.error('Error toggling like:', error)
      }
    },

    async addComment() {
      if (!this.newComment.trim()) return

      if (!this.authStore.isAuthenticated) {
        this.$router.push('/login')
        return
      }

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch(`/api/posts/${this.post.id}/comments`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            content: this.newComment,
          }),
        })

        const data = await response.json()
        if (data.success) {
          this.comments.unshift(data.comment)
          this.post.comments_count++
          this.newComment = ''
        }
      } catch (error) {
        console.error('Error adding comment:', error)
      }
    },

    focusComment() {
      document.querySelector('.comment-input-container textarea')?.focus()
    },

    sharePost() {
      if (navigator.share) {
        navigator.share({
          title: this.post.title,
          text: this.post.content.substring(0, 100),
          url: window.location.href,
        })
      } else {
        navigator.clipboard.writeText(window.location.href)
        alert('Ссылка скопирована в буфер обмена!')
      }
    },

    likeComment(commentId) {
      console.log('Like comment:', commentId)
    },

    replyToComment(comment) {
      this.newComment = `@${comment.author.username} `
      this.focusComment()
    },

    toggleSave() {
      console.log('Toggle save')
    },
  },
}
</script>

<style scoped>
.post-detail-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 3rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(138, 43, 226, 0.3);
  border-radius: 50%;
  border-top-color: #8a2be2;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.back-link {
  display: inline-block;
  color: #8a2be2;
  text-decoration: none;
  margin-bottom: 1.5rem;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background 0.3s;
}

.back-link:hover {
  background: rgba(138, 43, 226, 0.1);
}

.post-card.detailed {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.post-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.author-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.post-meta {
  flex: 1;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.3rem;
}

.author-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: white;
}

.author-badge {
  color: #1e90ff;
  font-size: 1rem;
}

.post-time {
  color: #888;
  font-size: 0.9rem;
}

.post-content {
  margin-bottom: 2rem;
}

.post-title {
  font-size: 2rem;
  color: white;
  margin-bottom: 1rem;
}

.post-type {
  display: inline-block;
  background: rgba(138, 43, 226, 0.2);
  color: #8a2be2;
  padding: 0.3rem 1rem;
  border-radius: 15px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.post-text {
  color: #b0b0b0;
  line-height: 1.8;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.track-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border-left: 3px solid #8a2be2;
}

.track-icon {
  font-size: 1.5rem;
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

.post-stats {
  display: flex;
  gap: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  margin-bottom: 1.5rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-icon {
  font-size: 1.2rem;
}

.stat-value {
  font-weight: bold;
  color: white;
}

.stat-label {
  color: #888;
}

.post-actions {
  display: flex;
  gap: 1rem;
  padding: 1.5rem 0;
  border-top: 1px solid #333;
  border-bottom: 1px solid #333;
}

.action-btn {
  flex: 1;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 10px;
  color: #b0b0b0;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.like-btn:hover {
  border-color: #ff4757;
  color: #ff4757;
}

.comment-btn:hover {
  border-color: #1e90ff;
  color: #1e90ff;
}

.share-btn:hover {
  border-color: #2ed573;
  color: #2ed573;
}

.save-btn:hover {
  border-color: #ffa502;
  color: #ffa502;
}

.comments-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.comments-section h2 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.add-comment {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.comment-user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.comment-input-container {
  flex: 1;
}

.comment-input-container textarea {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid #444;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  font-family: inherit;
  margin-bottom: 0.5rem;
  resize: vertical;
}

.comment-input-container textarea:focus {
  outline: none;
  border-color: #8a2be2;
}

.submit-comment-btn {
  padding: 0.5rem 1.5rem;
  background: #8a2be2;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  float: right;
}

.submit-comment-btn:hover {
  background: #7a1be2;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comment {
  display: flex;
  gap: 1rem;
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
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 1rem;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: 600;
  color: white;
  font-size: 0.95rem;
}

.comment-time {
  color: #888;
  font-size: 0.85rem;
}

.comment-text {
  color: #b0b0b0;
  line-height: 1.5;
  margin-bottom: 0.8rem;
}

.comment-actions {
  display: flex;
  gap: 1rem;
}

.comment-action-btn {
  background: transparent;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 0.85rem;
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
}

.comment-action-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #8a2be2;
}

.similar-posts {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 15px;
  padding: 2rem;
}

.similar-posts h2 {
  color: white;
  margin-bottom: 1.5rem;
}

.similar-posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.similar-post {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 1.5rem;
  text-decoration: none;
  transition:
    transform 0.3s,
    background 0.3s;
}

.similar-post:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.08);
}

.similar-post h3 {
  color: white;
  margin-bottom: 0.8rem;
  font-size: 1.1rem;
}

.similar-post p {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.similar-post-meta {
  display: flex;
  justify-content: space-between;
  color: #888;
  font-size: 0.85rem;
}

.not-found {
  text-align: center;
  padding: 4rem 2rem;
}

.not-found h2 {
  font-size: 2rem;
  color: white;
  margin-bottom: 1rem;
}

.not-found p {
  color: #b0b0b0;
  margin-bottom: 2rem;
}

.btn-primary {
  display: inline-block;
  padding: 0.8rem 2rem;
  background: linear-gradient(90deg, #8a2be2, #4b0082);
  color: white;
  text-decoration: none;
  border-radius: 10px;
  transition: transform 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .post-title {
    font-size: 1.5rem;
  }

  .post-stats {
    flex-direction: column;
    gap: 1rem;
  }

  .post-actions {
    flex-wrap: wrap;
  }

  .action-btn {
    flex: none;
    width: calc(50% - 0.5rem);
  }

  .add-comment {
    flex-direction: column;
  }

  .comment-user-avatar {
    align-self: flex-start;
  }
}
</style>
