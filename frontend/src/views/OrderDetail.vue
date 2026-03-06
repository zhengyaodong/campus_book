<template>
  <div class="order-detail-page">
    <div class="container" v-loading="loading">
      <template v-if="order">
        <div class="card">
          <div class="header">
            <h2>订单详情</h2>
            <span class="status">{{ getStatusText(order.status) }}</span>
          </div>
          <div class="info-section">
            <div class="info-row">
              <span class="label">订单号：</span>
              <span>{{ order.order_no }}</span>
            </div>
            <div class="info-row">
              <span class="label">创建时间：</span>
              <span>{{ order.created_at }}</span>
            </div>
          </div>
          <el-divider />
          <div class="info-section">
            <h3>书籍信息</h3>
            <div class="book-info">
              <div class="info-row">
                <span class="label">书名：</span>
                <span>{{ order.book_title }}</span>
              </div>
              <div class="info-row">
                <span class="label">价格：</span>
                <span>¥{{ order.book_price }}</span>
              </div>
            </div>
          </div>
          <el-divider />
          <div class="info-section">
            <h3>收货信息</h3>
            <div class="info-row">
              <span class="label">收货人：</span>
              <span>{{ order.address?.receiver }}</span>
            </div>
            <div class="info-row">
              <span class="label">电话：</span>
              <span>{{ order.address?.phone }}</span>
            </div>
            <div class="info-row">
              <span class="label">地址：</span>
              <span>{{ order.address?.address }}</span>
            </div>
          </div>
          <el-divider />
          <div class="total-section">
            <span>总价：</span>
            <span class="total-price">¥{{ order.total_price }}</span>
          </div>
          <div class="actions">
            <el-button v-if="order.status === 1" @click="handleCancel">取消订单</el-button>
            <el-button v-if="order.status === 3" type="primary" @click="handleConfirm">确认收货</el-button>
            <el-button @click="$router.back()">返回</el-button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const order = ref(null)

const statusMap = {
  1: '待付款',
  2: '待发货',
  3: '待收货',
  4: '已完成',
  5: '已取消'
}

const getStatusText = (status) => statusMap[status] || '未知'

const loadOrder = async () => {
  loading.value = true
  try {
    const res = await api.getOrder(route.params.id)
    if (res.code === 200) {
      order.value = res.data
    }
  } catch (error) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

const handleCancel = async () => {
  try {
    await ElMessageBox.confirm('确定要取消该订单吗？', '提示', { type: 'warning' })
    const res = await api.cancelOrder(order.value.id)
    if (res.code === 200) {
      ElMessage.success('订单已取消')
      loadOrder()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error)
    }
  }
}

const handleConfirm = async () => {
  try {
    await ElMessageBox.confirm('确定已收到货物吗？', '提示', { type: 'warning' })
    const res = await api.confirmOrder(order.value.id)
    if (res.code === 200) {
      ElMessage.success('确认收货成功')
      loadOrder()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error)
    }
  }
}

onMounted(() => {
  userStore.checkLogin()
  loadOrder()
})
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.card {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
}

.status {
  color: #409eff;
  font-weight: 500;
  font-size: 16px;
}

.info-section {
  margin-bottom: 20px;
}

.info-section h3 {
  margin-bottom: 15px;
  font-size: 16px;
}

.info-row {
  display: flex;
  margin-bottom: 10px;
}

.info-row .label {
  color: #999;
  width: 80px;
}

.total-section {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  font-size: 18px;
  margin: 20px 0;
}

.total-price {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
  margin-left: 10px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
