<template>
  <div class="search-page">
    <div class="container">
      <div class="search-bar">
        <el-input
          v-model="keyword"
          placeholder="搜索书籍..."
          @keyup.enter="handleSearch"
          style="width: 400px"
        >
          <template #append>
            <el-button :icon="Search" @click="handleSearch" />
          </template>
        </el-input>
      </div>
      <div class="filters">
        <span>筛选：</span>
        <el-select v-model="filters.category" placeholder="分类" clearable @change="handleSearch" style="width: 120px">
          <el-option label="教材类" value="教材类" />
          <el-option label="考研资料" value="考研资料" />
          <el-option label="课外阅读" value="课外阅读" />
          <el-option label="其他" value="其他" />
        </el-select>
        <el-select v-model="filters.condition" placeholder="成色" clearable @change="handleSearch" style="width: 120px">
          <el-option label="全新" value="全新" />
          <el-option label="九成新" value="九成新" />
          <el-option label="八成新" value="八成新" />
          <el-option label="七成新" value="七成新" />
          <el-option label="及以下" value="及以下" />
        </el-select>
        <el-input-number v-model="filters.minPrice" placeholder="最低价" @change="handleSearch" style="width: 120px" />
        <span>-</span>
        <el-input-number v-model="filters.maxPrice" placeholder="最高价" @change="handleSearch" style="width: 120px" />
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
      <el-empty v-if="!loading && books.length === 0" description="未找到相关书籍" />
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="page"
          :page-size="20"
          :total="total"
          layout="prev, pager, next"
          @current-change="handleSearch"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const route = useRoute()
const userStore = useUserStore()

const keyword = ref(route.query.keyword || '')
const books = ref([])
const page = ref(1)
const total = ref(0)
const loading = ref(false)
const filters = reactive({
  category: '',
  condition: '',
  minPrice: null,
  maxPrice: null
})

const handleSearch = async () => {
  loading.value = true
  try {
    const params = { page: page.value }
    if (keyword.value) params.keyword = keyword.value
    if (filters.category) params.category = filters.category
    if (filters.condition) params.condition = filters.condition
    if (filters.minPrice !== null) params.min_price = filters.minPrice
    if (filters.maxPrice !== null) params.max_price = filters.maxPrice

    const res = await api.searchBooks(params)
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

onMounted(() => {
  userStore.checkLogin()
  handleSearch()
})
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-bar {
  margin-bottom: 20px;
}

.filters {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
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
  font-weight: bold;
  color: #f56c6c;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
</style>
