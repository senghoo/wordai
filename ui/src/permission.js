import router from './router'
import store from './store'
import {getToken} from './store'

import { Message } from 'element-ui'

const whiteList = ['/login']

router.beforeEach((to, from, next) => {
  if (getToken()) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else {
      store.dispatch('getUserInfo').then(res => {
        next()
      }).catch((err) => {
        store.dispatch('logOut').then(() => {
          Message.error(err || 'Verification failed, please login again')
          next({ path: '/' })
        })
      })
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      next('/login')
    }
  }
})
