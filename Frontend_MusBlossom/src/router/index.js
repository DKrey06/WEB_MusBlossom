import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { title: 'MusBlossom - Главная' },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { title: 'Вход в MusBlossom', guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { title: 'Регистрация в MusBlossom', guestOnly: true },
    },
    {
      path: '/posts',
      name: 'posts',
      component: () => import('@/views/PostsView.vue'),
      meta: { title: 'Сообщество' },
    },
    {
      path: '/posts/:id',
      name: 'post-detail',
      component: () => import('@/views/PostDetailView.vue'),
      meta: { title: 'Пост' },
    },
    {
      path: '/create-post',
      name: 'create-post',
      component: () => import('@/views/CreatePostView.vue'),
      meta: { title: 'Создать пост', requiresAuth: true },
    },
    {
      path: '/edit-post/:id',
      name: 'edit-post',
      component: () => import('@/views/EditPostView.vue'),
      meta: { title: 'Редактировать пост', requiresAuth: true },
    },
    {
      path: '/playlists',
      name: 'playlists',
      component: () => import('@/views/PlaylistsView.vue'),
      meta: { title: 'Плейлисты' },
    },
    {
      path: '/playlists/:id',
      name: 'playlist-detail',
      component: () => import('@/views/PlaylistDetailView.vue'),
      meta: { title: 'Плейлист' },
    },
    {
      path: '/create-playlist',
      name: 'create-playlist',
      component: () => import('@/views/CreatePlaylistView.vue'),
      meta: { title: 'Создать плейлист', requiresAuth: true },
    },
    {
      path: '/concerts',
      name: 'concerts',
      component: () => import('@/views/ConcertsView.vue'),
      meta: { title: 'Концерты' },
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('@/views/SearchView.vue'),
      meta: { title: 'Поиск' },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      meta: { title: 'Профиль', requiresAuth: true },
    },
    {
      path: '/profile/:username',
      name: 'user-profile',
      component: () => import('@/views/UserProfileView.vue'),
      meta: { title: 'Профиль пользователя' },
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue'),
      meta: { title: 'Настройки', requiresAuth: true },
    },
    {
      path: '/events',
      name: 'events',
      component: () => import('@/views/EventsView.vue'),
      meta: { title: 'События' },
    },
    {
      path: '/friends',
      name: 'friends',
      component: () => import('@/views/FriendsView.vue'),
      meta: { title: 'Друзья', requiresAuth: true },
    },
    {
      path: '/room/:roomId',
      name: 'music-room',
      component: () => import('@/views/MusicRoomView.vue'),
      meta: { title: 'Музыкальная комната', requiresAuth: true },
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/AboutView.vue'),
      meta: { title: 'О проекте' },
    },
    {
      path: '/feedback',
      name: 'feedback',
      component: () => import('@/views/FeedbackView.vue'),
      meta: { title: 'Обратная связь' },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
      meta: { title: 'Страница не найдена' },
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  },
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.title) {
    document.title = to.meta.title
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    next('/')
    return
  }

  if (authStore.isAuthenticated && !authStore.user) {
    authStore.fetchUser()
  }

  next()
})

router.afterEach((to, from) => {
  console.log(`Navigated from ${from.path} to ${to.path}`)
})

export default router
