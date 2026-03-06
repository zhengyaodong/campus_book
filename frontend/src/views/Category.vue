<template>
  <div class="category-page">
    <!-- 顶部导航 -->
    <header class="header">
      <div class="container">
        <div class="header-left">
          <router-link to="/" class="logo">📚 校园二手书</router-link>
        </div>
        <div class="header-center">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索书籍..."
            @keyup.enter="handleSearch"
            class="search-input"
          >
            <template #append>
              <el-button :icon="Search" @click="handleSearch" />
            </template>
          </el-input>
        </div>
        <div class="header-right">
          <el-button @click="$router.push('/publish')">发布书籍</el-button>
          <template v-if="userStore.userInfo">
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                {{ userStore.userInfo.nickname }}
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="orders">我的订单</el-dropdown-item>
                  <el-dropdown-item command="address">收货地址</el-dropdown-item>
                  <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                  <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button @click="$router.push('/login')">登录</el-button>
            <el-button type="primary" @click="$router.push('/register')">注册</el-button>
          </template>
        </div>
      </div>
    </header>

    <!-- 分类导航 -->
    <nav class="category-nav">
      <div class="container">
        <router-link to="/category" class="category-item">全部</router-link>
        <router-link
          v-for="cat in categories"
          :key="cat.value"
          :to="`/category/${cat.value}`"
          class="category-item"
        >
          {{ cat.label }}
        </router-link>
      </div>
    </nav>

    <div class="container">
      <div class="page-header">
        <h2>{{ categoryName }}</h2>
      </div>
      <el-row :gutter="20" v-loading="loading">
        <el-col
          :xs="12" :sm="8" :md="6" :lg="4"
          v-for="book in books"
          :key="book.id"
        >
          <div class="book-card" @click="$router.push(`/book/${book.id}`)">
            <div class="book-cover">
              <img :src="book.images?.[0] || '/default-book.svg'" :alt="book.title" />
            </div>
            <div class="book-info">
              <h3 class="book-title">{{ book.title }}</h3>
              <p class="book-author">{{ book.author || '未知作者' }}</p>
              <div class="book-meta">
                <span class="book-condition">{{ book.condition }}</span>
                <span class="book-price">¥{{ book.price }}</span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
      <el-empty v-if="!loading && books.length === 0" description="暂无书籍" />
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="page"
          :page-size="20"
          :total="total"
          layout="prev, pager, next"
          @current-change="loadBooks"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Search, ArrowDown } from '@element-plus/icons-vue'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const searchKeyword = ref('')

const categories = [
  { label: '教材类', value: '教材类' },
  { label: '考研资料', value: '考研资料' },
  { label: '课外阅读', value: '课外阅读' },
  { label: '其他', value: '其他' }
]

const books = ref([])
const page = ref(1)
const total = ref(0)
const loading = ref(false)

const categoryName = computed(() => {
  const map = {
    '教材类': '教材类',
    '考研资料': '考研资料',
    '课外阅读': '课外阅读',
    '其他': '其他'
  }
  return map[route.params.type] || '全部'
})

const loadBooks = async () => {
  loading.value = true
  try {
    const params = { page: page.value }
    if (route.params.type) {
      params.category = route.params.type
    }
    const res = await api.getBooks(params)
    if (res.code === 200) {
      books.value = res.data.items.map(book => ({
        ...book,
        images: typeof book.images === 'string' ? JSON.parse(book.images) : book.images || []
      }))
      total.value = res.data.total
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  router.push({ path: '/search', query: { keyword: searchKeyword.value } })
}

const handleCommand = (command) => {
  if (command === 'logout') {
    userStore.logout()
  } else {
    router.push(`/${command}`)
  }
}

watch(() => route.params.type, () => {
  page.value = 1
  loadBooks()
})

onMounted(() => {
  userStore.checkLogin()
  loadBooks()
})
</script>

<style scoped>
.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 15px 0;
}

.header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  text-decoration: none;
}

.header-center {
  flex: 1;
  max-width: 400px;
  margin: 0 20px;
}

.search-input {
  width: 100%;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 5px 10px;
}

.category-nav {
  background: #fff;
  margin-bottom: 20px;
}

.category-nav .container {
  display: flex;
  gap: 30px;
  padding: 15px 20px;
  overflow-x: auto;
}

.category-item {
  text-decoration: none;
  color: #666;
  white-space: nowrap;
  transition: color 0.3s;
}

.category-item:hover,
.category-item.router-link-active {
  color: #409eff;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 20px;
  font-weight: 600;
}

.book-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  margin-bottom: 20px;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.book-cover {
  height: 180px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.book-cover img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.book-info {
  padding: 12px;
}

.book-title {
  font-size: 14px;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 5px;
}

.book-author {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.book-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.book-condition {
  font-size: 12px;
  color: #67c23a;
  background: #f0f9eb;
  padding: 2px 8px;
  border-radius: 4px;
}

.book-price {
  font-size: 16px;
  color: #f56c6c;
  font-weight: 600;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
</style>
