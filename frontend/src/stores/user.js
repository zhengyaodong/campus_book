import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useUserStore = defineStore('user', () => {
  const userInfo = ref(null)
  const token = ref(localStorage.getItem('token') || '')

  // 设置用户信息
  const setUserInfo = (info) => {
    userInfo.value = info
    if (info) {
      localStorage.setItem('userInfo', JSON.stringify(info))
    } else {
      localStorage.removeItem('userInfo')
    }
  }

  // 登录
  const login = async (username, password) => {
    const res = await api.login({ username, password })
    if (res.code === 200) {
      setUserInfo(res.data)
      token.value = res.data.id
      localStorage.setItem('token', res.data.id)
      return true
    }
    return false
  }

  // 注册
  const register = async (data) => {
    const res = await api.register(data)
    if (res.code === 200) {
      setUserInfo(res.data)
      token.value = res.data.id
      localStorage.setItem('token', res.data.id)
      return true
    }
    return false
  }

  // 登出
  const logout = () => {
    userInfo.value = null
    token.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  // 检查登录状态
  const checkLogin = () => {
    const userInfoStr = localStorage.getItem('userInfo')
    const tokenStr = localStorage.getItem('token')
    if (userInfoStr && tokenStr) {
      userInfo.value = JSON.parse(userInfoStr)
      token.value = tokenStr
      return true
    }
    return false
  }

  // 更新用户信息
  const updateProfile = async (data) => {
    const res = await api.updateProfile({ user_id: userInfo.value.id, ...data })
    if (res.code === 200) {
      setUserInfo(res.data)
      return true
    }
    return false
  }

  return {
    userInfo,
    token,
    setUserInfo,
    login,
    register,
    logout,
    checkLogin,
    updateProfile
  }
})
