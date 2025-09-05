import axios from 'axios'
import store from '../store'
import { ElMessage } from 'element-plus'

// 创建axios实例
const request = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 添加token到请求头
    const token = store.state.auth.token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          store.dispatch('auth/logout')
          ElMessage.error('登录已过期，请重新登录')
          break
        case 403:
          ElMessage.error('没有权限访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(data.error || '请求失败')
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

// API接口定义
const api = {
  // 认证相关
  auth: {
    login: (credentials) => request.post('/auth/login', credentials),
    register: (userData) => request.post('/auth/register', userData),
    getProfile: () => request.get('/auth/profile'),
    updateProfile: (profileData) => request.put('/auth/profile', profileData)
  },

  // 活动相关
  activities: {
    getActivities: (params) => request.get('/activities', { params }),
    getActivity: (id) => request.get(`/activities/${id}`),
    createActivity: (activityData) => request.post('/activities', activityData),
    registerActivity: (id, data) => request.post(`/activities/${id}/register`, data),
    unregisterActivity: (id) => request.delete(`/activities/${id}/unregister`)
  },

  // 用户相关
  users: {
    getMyRegistrations: (params) => request.get('/users/my-registrations', { params }),
    getMyActivities: (params) => request.get('/users/my-activities', { params }),
    getStatistics: () => request.get('/users/statistics'),
    checkIn: (registrationId) => request.post(`/users/check-in/${registrationId}`),
    completeActivity: (registrationId, data) => request.post(`/users/complete/${registrationId}`, data)
  }
}

export default api