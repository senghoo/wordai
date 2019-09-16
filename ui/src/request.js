import axios from 'axios'
import {MessageBox} from 'element-ui'
import store from './store'
import { getToken } from './store'

const service = axios.create({
  baseURL: process.env.BASE_API
})

var lastRefresh = (new Date()).getTime()
service.interceptors.request.use(config => {
  if (getToken()) {
    if (!config.headers['Authorization']){
      config.headers['Authorization'] = 'Bearer ' + getToken() // 让每个请求携带自定义token 请根据实际情况自行修改
    }
    var now = (new Date()).getTime()
    // debugger;
    if (now - lastRefresh > 1 * 60 * 1000 && config.url !== '/token/refresh' && config.url !== '/login') {
      store.dispatch('refreshJWT').then(() => {
        lastRefresh = now
      })
    }
  }
  return config
}, error => {
  // Do something with request error
  console.log(error) // for debug
  Promise.reject(error)
})

service.interceptors.response.use(

  response => {
    return response
  },
  error => {
    const req = error.request
    const res = error.response
    const url = new URL(req.responseURL)
    if (res.status === 401 && url.pathname !== '/login') {
      MessageBox.confirm('你已被登出', '确定登出', {
        confirmButtonText: '重新登录',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        store.dispatch('logOut').then(() => {
          location.reload()// 为了重新实例化vue-router对象 避免bug
        })
      })
    }
    return Promise.reject(error)
  }
)

export default service
