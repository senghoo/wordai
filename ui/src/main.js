// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueAxios from 'vue-axios'
import axios from 'axios'
import underscore from 'vue-underscore'


import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import App from './App'
import router from './router'
import store from './store'
import request from './request'
import '@/permission'



Vue.use(ElementUI)
Vue.use(VueAxios, request)
Vue.use(underscore)

import moment from 'moment-timezone'
moment.tz.setDefault("UTC")
require('moment/locale/zh-cn')
Vue.use(require('vue-moment'), {
  moment
})

Vue.config.productionTip = false


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
