import axios from 'axios'

const api = axios.create({
  // baseURL: '/api',
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.msg || '请求失败'
    return Promise.reject(message)
  }
)

export default {
  // 用户相关
  register(data) {
    return api.post('/user/register', data)
  },
  login(data) {
    return api.post('/user/login', data)
  },
  getProfile(userId) {
    return api.get('/user/profile', { params: { user_id: userId } })
  },
  updateProfile(data) {
    return api.put('/user/profile', data)
  },

  // 书籍相关
  getBooks(params) {
    return api.get('/books', { params })
  },
  getBook(id) {
    return api.get(`/books/${id}`)
  },
  createBook(data) {
    return api.post('/books', data)
  },
  updateBook(id, data) {
    return api.put(`/books/${id}`, data)
  },
  deleteBook(id) {
    return api.delete(`/books/${id}`)
  },
  searchBooks(params) {
    return api.get('/books/search', { params })
  },

  // 订单相关
  createOrder(data) {
    return api.post('/orders', data)
  },
  getOrders(params) {
    return api.get('/orders', { params })
  },
  getOrder(id) {
    return api.get(`/orders/${id}`)
  },
  cancelOrder(id) {
    return api.put(`/orders/${id}/cancel`)
  },
  confirmOrder(id) {
    return api.put(`/orders/${id}/confirm`)
  },

  // 地址相关
  getAddresses(userId) {
    return api.get('/addresses', { params: { user_id: userId } })
  },
  createAddress(data) {
    return api.post('/addresses', data)
  },
  updateAddress(id, data) {
    return api.put(`/addresses/${id}`, data)
  },
  deleteAddress(id) {
    return api.delete(`/addresses/${id}`)
  }
}
