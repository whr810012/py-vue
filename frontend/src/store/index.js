import { createStore } from 'vuex'
import auth from './modules/auth'
import activities from './modules/activities'

export default createStore({
  modules: {
    auth,
    activities
  }
})