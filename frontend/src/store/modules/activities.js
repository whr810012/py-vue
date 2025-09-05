import api from '../../api'

const state = {
  activities: [],
  currentActivity: null,
  myRegistrations: [],
  myActivities: [],
  loading: false,
  pagination: {
    total: 0,
    pages: 0,
    currentPage: 1
  }
}

const mutations = {
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ACTIVITIES(state, { activities, pagination }) {
    state.activities = activities
    if (pagination) {
      state.pagination = pagination
    }
  },
  SET_CURRENT_ACTIVITY(state, activity) {
    state.currentActivity = activity
  },
  SET_MY_REGISTRATIONS(state, registrations) {
    state.myRegistrations = registrations
  },
  SET_MY_ACTIVITIES(state, activities) {
    state.myActivities = activities
  },
  ADD_ACTIVITY(state, activity) {
    state.activities.unshift(activity)
  },
  UPDATE_ACTIVITY(state, updatedActivity) {
    const index = state.activities.findIndex(a => a.id === updatedActivity.id)
    if (index !== -1) {
      state.activities.splice(index, 1, updatedActivity)
    }
  }
}

const actions = {
  async fetchActivities({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await api.activities.getActivities(params)
      const { activities, total, pages, current_page } = response.data
      
      commit('SET_ACTIVITIES', {
        activities,
        pagination: {
          total,
          pages,
          currentPage: current_page
        }
      })
      
      return response
    } catch (error) {
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchActivity({ commit }, activityId) {
    commit('SET_LOADING', true)
    try {
      const response = await api.activities.getActivity(activityId)
      const activity = response.data.activity
      
      commit('SET_CURRENT_ACTIVITY', activity)
      return response
    } catch (error) {
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async createActivity({ commit }, activityData) {
    try {
      const response = await api.activities.createActivity(activityData)
      const activity = response.data.activity
      
      commit('ADD_ACTIVITY', activity)
      return response
    } catch (error) {
      throw error
    }
  },

  async registerActivity({ commit }, { activityId, notes }) {
    try {
      const response = await api.activities.registerActivity(activityId, { notes })
      return response
    } catch (error) {
      throw error
    }
  },

  async unregisterActivity({ commit }, activityId) {
    try {
      const response = await api.activities.unregisterActivity(activityId)
      return response
    } catch (error) {
      throw error
    }
  },

  async fetchMyRegistrations({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await api.users.getMyRegistrations(params)
      const registrations = response.data.registrations
      
      commit('SET_MY_REGISTRATIONS', registrations)
      return response
    } catch (error) {
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async fetchMyActivities({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await api.users.getMyActivities(params)
      const activities = response.data.activities
      
      commit('SET_MY_ACTIVITIES', activities)
      return response
    } catch (error) {
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async checkIn({ commit }, registrationId) {
    try {
      const response = await api.users.checkIn(registrationId)
      return response
    } catch (error) {
      throw error
    }
  },

  async completeActivity({ commit }, { registrationId, rating, feedback }) {
    try {
      const response = await api.users.completeActivity(registrationId, {
        rating,
        feedback
      })
      return response
    } catch (error) {
      throw error
    }
  }
}

const getters = {
  activities: state => state.activities,
  currentActivity: state => state.currentActivity,
  myRegistrations: state => state.myRegistrations,
  myActivities: state => state.myActivities,
  loading: state => state.loading,
  pagination: state => state.pagination
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}