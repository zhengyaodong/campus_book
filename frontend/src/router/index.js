import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import BookDetail from '@/views/BookDetail.vue'
import Publish from '@/views/Publish.vue'
import Category from '@/views/Category.vue'
import Search from '@/views/Search.vue'
import Orders from '@/views/Orders.vue'
import OrderDetail from '@/views/OrderDetail.vue'
import Address from '@/views/Address.vue'
import Profile from '@/views/Profile.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/book/:id', name: 'BookDetail', component: BookDetail },
  { path: '/publish', name: 'Publish', component: Publish },
  { path: '/category/:type?', name: 'Category', component: Category },
  { path: '/search', name: 'Search', component: Search },
  { path: '/orders', name: 'Orders', component: Orders },
  { path: '/order/:id', name: 'OrderDetail', component: OrderDetail },
  { path: '/address', name: 'Address', component: Address },
  { path: '/profile', name: 'Profile', component: Profile }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
