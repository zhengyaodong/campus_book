<template>
  <div class="orders-page">
    <div class="container">
      <h2>我的订单</h2>
      <el-tabs v-model="activeTab" @tab-change="loadOrders">
        <el-tab-pane label="全部" name="" />
        <el-tab-pane label="待付款" name="1" />
        <el-tab-pane label="待发货" name="2" />
        <el-tab-pane label="待收货" name="3" />
        <el-tab-pane label="已完成" name="4" />
      </el-tabs>
      <div class="order-list" v-loading="loading">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <span class="order-no">订单号：{{ order.order_no }}</span>
            <span class="order-status">{{ getStatusText(order.status) }}</span>
          </div>
          <div class="order-body" @click="$router.push(`/order/${order.id}`)">
            <div class="book-info">
              <h4>{{ order.book_title }}</h4>
              <p class="price">¥{{ order.book_price }}</p>
            </div>
            <div class="order-total">
              <span>总价：</span>
              <span class="total-price">¥{{ order.total_price }}</span>
            </div>
          </div>
          <div class="order-footer">
            <span class="order-time">{{ order.created_at }}</span>
            <div class="actions">
              <el-button v-if="order.status === 1" size="small" @click.stop="handleCancel(order.id)">取消订单</el-button>
              <el-button v-if="order.status === 3" type="primary" size="small" @click.stop="handleConfirm(order.id)">确认收货</el-button>
              <el-button size="small" @click.stop="$router.push(`/order/${order.id}`)">查看详情</el-button>
            </div>
          </div>
        </div>
        <el-empty v-if="!loading && orders.length === 0" description="暂无订单" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const userStore = useUserStore()

const activeTab = ref('')
const orders = ref([])
const loading = ref(false)

const statusMap = {
  1: '待付款',
  2: '待发货',
  3: '待收货',
  4: '已完成',
  5: '已取消'
}

const getStatusText = (status) => statusMap[status] || '未知'

const loadOrders = async () => {
  if (!userStore.userInfo) return

  loading.value = true
  try {
    const params = { user_id: userStore.userInfo.id }
    if (activeTab.value) {
      params.status = parseInt(activeTab.value)
    }
    const res = await api.getOrders(params)
    if (res.code === 200) {
      orders.value = res.data.items
    }
  } catch (error) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

const handleCancel = async (orderId) => {
  try {
    await ElMessageBox.confirm('确定要取消该订单吗？', '提示', { type: 'warning' })
    const res = await api.cancelOrder(orderId)
    if (res.code === 200) {
      ElMessage.success('订单已取消')
      loadOrders()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error)
    }
  }
}

const handleConfirm = async (orderId) => {
  try {
    await ElMessageBox.confirm('确定已收到货物吗？', '提示', { type: 'warning' })
    const res = await api.confirmOrder(orderId)
    if (res.code === 200) {
      ElMessage.success('确认收货成功')
      loadOrders()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error)
    }
  }
}

onMounted(() => {
  userStore.checkLogin()
  if (userStore.userInfo) {
    loadOrders()
  }
})
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.container h2 {
  margin-bottom: 20px;
}

.order-card {
  background: #fff;
  border-radius: 8px;
  margin-bottom: 15px;
  overflow: hidden;
}

.order-header {
  display: flex;
  justify-content: space-between;
  padding: 15px 20px;
  background: #f5f5f5;
}

.order-no {
  color: #999;
  font-size: 12px;
}

.order-status {
  color: #409eff;
  font-weight: 500;
}

.order-body {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  cursor: pointer;
}

.book-info h4 {
  margin-bottom: 5px;
}

.book-info .price {
  color: #999;
}

.order-total {
  text-align: right;
}

.total-price {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-top: 1px solid #eee;
}

.order-time {
  color: #999;
  font-size: 12px;
}

.actions {
  display: flex;
  gap: 10px;
}
</style>
