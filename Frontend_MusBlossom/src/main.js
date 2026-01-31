import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'
import './assets/global.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

console.log('API Base URL:', API_BASE_URL)

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,
})

axiosInstance.interceptors.request.use(
  (config) => {
    console.log(`Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`)
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  },
)

axiosInstance.interceptors.response.use(
  (response) => {
    console.log(`Response ${response.status}: ${response.config.url}`)
    return response.data
  },
  async (error) => {
    console.error('Response error:', error.response?.status, error.config?.url)
    return Promise.reject(error)
  },
)

const app = createApp(App)
const pinia = createPinia()

app.config.globalProperties.$axios = axiosInstance
app.config.globalProperties.$api = axiosInstance

app.use(pinia)
app.use(router)

app.mount('#app')
