<template>
  <div class="book-detail-page">
    <div class="container" v-loading="loading">
      <template v-if="book">
        <div class="book-header">
          <div class="book-images">
            <el-carousel height="400px" v-if="book.images && book.images.length > 0">
              <el-carousel-item v-for="(img, index) in book.images" :key="index">
                <img :src="img" :alt="book.title" />
              </el-carousel-item>
            </el-carousel>
            <div class="no-image" v-else>
              <span>暂无图片</span>
            </div>
          </div>
          <div class="book-info">
            <h1>{{ book.title }}</h1>
            <div class="info-row">
              <span class="label">作者：</span>
              <span>{{ book.author || '未知' }}</span>
            </div>
            <div class="info-row">
              <span class="label">ISBN：</span>
              <span>{{ book.isbn || '未知' }}</span>
            </div>
            <div class="info-row">
              <span class="label">分类：</span>
              <el-tag>{{ book.category }}</el-tag>
            </div>
            <div class="info-row">
              <span class="label">成色：</span>
              <el-tag type="success">{{ book.condition }}</el-tag>
            </div>
            <div class="info-row">
              <span class="label">交易方式：</span>
              <span>{{ book.delivery_type }}</span>
            </div>
            <div class="info-row">
              <span class="label">库存：</span>
              <span>{{ book.stock }}本</span>
            </div>
            <div class="price-row">
              <span class="price">¥{{ book.price }}</span>
            </div>
            <div class="action-row">
              <el-button type="primary" size="large" @click="handleBuy">
                立即购买
              </el-button>
              <el-button size="large" @click="$router.back()">返回</el-button>
            </div>
          </div>
        </div>
        <div class="book-desc">
          <h3>书籍描述</h3>
          <p>{{ book.description || '暂无描述' }}</p>
        </div>
        <div class="seller-info">
          <h3>卖家信息</h3>
          <div class="seller">
            <el-avatar :size="50">{{ book.seller_nickname?.[0] || '?' }}</el-avatar>
            <div class="seller-detail">
              <span class="nickname">{{ book.seller_nickname }}</span>
              <span class="time">发布于 {{ book.created_at }}</span>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- 购买弹窗 -->
    <el-dialog v-model="showBuyDialog" title="确认订单" width="500px">
      <el-form :model="orderForm" label-width="80px">
        <el-form-item label="收货地址">
          <el-select v-model="orderForm.addressId" placeholder="请选择收货地址" style="width: 100%">
            <el-option
              v-for="addr in addresses"
              :key="addr.id"
              :label="`${addr.receiver} - ${addr.address}`"
              :value="addr.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button text @click="$router.push('/address')">管理收货地址</el-button>
        </el-form-item>
        <el-divider />
        <div class="order-summary">
          <div class="summary-row">
            <span>书籍：</span>
            <span>{{ book?.title }}</span>
          </div>
          <div class="summary-row total">
            <span>总价：</span>
            <span class="price">¥{{ book?.price }}</span>
          </div>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="showBuyDialog = false">取消</el-button>
        <el-button type="primary" :loading="orderLoading" @click="submitOrder">提交订单</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const book = ref(null)
const showBuyDialog = ref(false)
const orderLoading = ref(false)
const addresses = ref([])
const orderForm = reactive({
  addressId: null
})

const loadBook = async () => {
  loading.value = true
  try {
    const res = await api.getBook(route.params.id)
    if (res.code === 200) {
      const data = res.data
      data.images = typeof data.images === 'string' ? JSON.parse(data.images) : data.images || []
      book.value = data
    }
  } catch (error) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

const loadAddresses = async () => {
  if (!userStore.userInfo) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  try {
    const res = await api.getAddresses(userStore.userInfo.id)
    if (res.code === 200) {
      addresses.value = res.data
      const defaultAddr = addresses.value.find(a => a.is_default === 1)
      if (defaultAddr) {
        orderForm.addressId = defaultAddr.id
      }
    }
  } catch (error) {
    console.error(error)
  }
}

const handleBuy = () => {
  if (!userStore.userInfo) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  if (book.value.stock < 1) {
    ElMessage.warning('库存不足')
    return
  }
  loadAddresses()
  showBuyDialog.value = true
}

const submitOrder = async () => {
  if (!orderForm.addressId) {
    ElMessage.warning('请选择收货地址')
    return
  }
  orderLoading.value = true
  try {
    const res = await api.createOrder({
      user_id: userStore.userInfo.id,
      book_id: book.value.id,
      address_id: orderForm.addressId
    })
    if (res.code === 200) {
      ElMessage.success('订单创建成功')
      showBuyDialog.value = false
      router.push('/orders')
    }
  } catch (error) {
    ElMessage.error(error)
  } finally {
    orderLoading.value = false
  }
}

onMounted(() => {
  userStore.checkLogin()
  loadBook()
})
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.book-header {
  display: flex;
  gap: 40px;
  background: #fff;
  padding: 30px;
  border-radius: 8px;
}

.book-images {
  width: 400px;
  flex-shrink: 0;
}

.book-images img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.no-image {
  height: 400px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.book-info {
  flex: 1;
}

.book-info h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.info-row {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.info-row .label {
  color: #999;
  margin-right: 10px;
}

.price-row {
  margin: 30px 0;
}

.price {
  font-size: 32px;
  font-weight: bold;
  color: #f56c6c;
}

.action-row {
  display: flex;
  gap: 15px;
}

.book-desc,
.seller-info {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  margin-top: 20px;
}

.book-desc h3,
.seller-info h3 {
  margin-bottom: 15px;
  font-size: 16px;
}

.seller {
  display: flex;
  align-items: center;
  gap: 15px;
}

.seller-detail {
  display: flex;
  flex-direction: column;
}

.seller-detail .nickname {
  font-weight: 500;
}

.seller-detail .time {
  font-size: 12px;
  color: #999;
}

.order-summary {
  padding: 10px 0;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.summary-row.total {
  font-weight: bold;
  font-size: 16px;
}

.summary-row .price {
  font-size: 18px;
}
</style>
