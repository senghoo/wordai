import Vue from 'vue'
import vuex from 'vuex'
import service from './request'
//import Cookies from 'js-cookie'

// Vue.use(service)
Vue.use(vuex)

const TokenKey = 'accessToken'
const refreshKey = 'refreshToken'

export function getToken () {
  return sessionStorage.getItem(TokenKey)
}
export function getRefreshToken () {
  return sessionStorage.getItem(refreshKey)
}

export function setToken (token) {
  return sessionStorage.setItem(TokenKey, token)
}
export function setRefreshTokens (token) {
  return sessionStorage.setItem(refreshKey, token)
}

export function removeToken () {
  sessionStorage.removeItem(refreshKey)
  return sessionStorage.removeItem(TokenKey)
}

export default new vuex.Store({
  state: {
    accessToken: '',
    refreshToken: '',
    wordlist: ''
  },
  getters: {
    accessToken: state => state.accessToken,
    refreshToken: state => state.refreshToken,
    username: (state, getters) => state.accessToken ? JSON.parse(atob(getters.accessToken.split('.')[1])) : null,
  },
  mutations: {
    setTokens (state, access) {
      // When this updates, the getters and anything bound to them updates as well.
      state.accessToken = access
    },
    setRefreshTokens (state, refresh) {
      // When this updates, the getters and anything bound to them updates as well.
      state.refreshToken = refresh
    },
    setWordList (state, wordlist) {
      state.wordList = wordlist
    }
  },
  actions: {
    fetchJWT ({ commit }, { username, password }) {
      return service({
        'method': 'POST',
        'url': '/login',
        'headers': {
          'Content-Type': 'application/json; charset=utf-8'
        },
        'data': {
          'username': username,
          'password': password
        }
      }).then(res => {
        commit('setTokens', res.data.access_token)
        commit('setRefreshTokens', res.data.refresh_token)
        setToken(res.data.access_token)
        setRefreshTokens(res.data.refresh_token)
      } )
    },
    refreshJWT ({ commit, state}) {
      return service({
        'method': 'POST',
        'url': '/token/refresh',
        'headers': {
          'Content-Type': 'application/json; charset=utf-8',
          'Authorization': 'Bearer ' + getRefreshToken()
        }
      }).then(res => {
        commit('setTokens', res.data.access_token)
        // commit('setRefreshTokens', res.data.refresh_token)
        setToken(res.data.access_token, res.data.refresh_token)
      })
    },
    getUserInfo ({commit, state}) {
      return service({
        'method': 'GET',
        'url': '/user/wordlist',
        'headers': {
          'Content-Type': 'application/json; charset=utf-8',
          'Authorization': 'Bearer ' + getToken()
        }
      }).then(res => {
        commit('setWordList', res.wordlist)
      })
    },
    logOut ({commit, state}) {
      return new Promise((resolve, reject) => {
        commit('setTokens', '', '')
        removeToken()
        resolve()
      })
    }
  }
})
