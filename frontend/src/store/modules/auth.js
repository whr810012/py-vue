import api from '../../api'

const state = {
  isLoggedIn: false,
  userInfo: null,
  token: localStorage.getItem('token') || null
}

const mutations = {
  SET_LOGIN_STATUS(state, status) {
    state.isLoggedIn = status
  },
  SET_USER_INFO(state, userInfo) {
    state.userInfo = userInfo
  },
  SET_TOKEN(state, token) {
    state.token = token
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }
}

const actions = {
  async login({ commit }, credentials) {
    try {
      const response = await api.auth.login(credentials)
      const { access_token, user } = response.data
      
      commit('SET_TOKEN', access_token)
      commit('SET_USER_INFO', user)
      commit('SET_LOGIN_STATUS', true)
      
      return response
    } catch (error) {
      throw error
    }
  },

  async register({ commit }, userData) {
    try {
      const response = await api.auth.register(userData)
      return response
    } catch (error) {
      throw error
    }
  },

  async checkAuth({ commit, state }) {
    if (!state.token) {
      return
    }
    
    try {
      const response = await api.auth.getProfile()
      const user = response.data.user
      
      commit('SET_USER_INFO', user)
      commit('SET_LOGIN_STATUS', true)
    } catch (error) {
      // Token无效，清除本地存储
      commit('SET_TOKEN', null)
      commit('SET_USER_INFO', null)
      commit('SET_LOGIN_STATUS', false)
    }
  },

  async updateProfile({ commit }, profileData) {
    try {
      const response = await api.auth.updateProfile(profileData)
      const user = response.data.user
      
      commit('SET_USER_INFO', user)
      return response
    } catch (error) {
      throw error
    }
  },

  logout({ commit }) {
    commit('SET_TOKEN', null)
    commit('SET_USER_INFO', null)
    commit('SET_LOGIN_STATUS', false)
  }
}

const getters = {
  isLoggedIn: state => state.isLoggedIn,
  userInfo: state => state.userInfo,
  token: state => state.token,
  userId: state => state.userInfo ? state.userInfo.id : null,
  userRole: state => state.userInfo ? state.userInfo.role : null
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}