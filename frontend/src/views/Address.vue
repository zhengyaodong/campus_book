<template>
  <div class="address-page">
    <div class="container">
      <div class="header">
        <h2>收货地址</h2>
        <el-button type="primary" @click="showDialog = true">新增地址</el-button>
      </div>
      <div class="address-list" v-loading="loading">
        <div v-for="addr in addresses" :key="addr.id" class="address-card">
          <div class="address-info">
            <div class="receiver">{{ addr.receiver }}</div>
            <div class="phone">{{ addr.phone }}</div>
            <div class="address">{{ addr.address }}</div>
            <el-tag v-if="addr.is_default === 1" type="success" size="small">默认</el-tag>
          </div>
          <div class="actions">
            <el-button text @click="handleEdit(addr)">编辑</el-button>
            <el-button text @click="handleSetDefault(addr.id)" v-if="addr.is_default !== 1">设为默认</el-button>
            <el-button text type="danger" @click="handleDelete(addr.id)">删除</el-button>
          </div>
        </div>
        <el-empty v-if="!loading && addresses.length === 0" description="暂无收货地址" />
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="showDialog" :title="isEdit ? '编辑地址' : '新增地址'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="收货人" prop="receiver">
          <el-input v-model="form.receiver" placeholder="请输入收货人姓名" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="form.address" type="textarea" :rows="2" placeholder="请输入详细地址" />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="form.isDefault">设为默认地址</el-checkbox>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const userStore = useUserStore()

const loading = ref(false)
const addresses = ref([])
const showDialog = ref(false)
const submitLoading = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const formRef = ref()
const form = reactive({
  receiver: '',
  phone: '',
  address: '',
  isDefault: false
})

const rules = {
  receiver: [{ required: true, message: '请输入收货人', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }]
}

const loadAddresses = async () => {
  if (!userStore.userInfo) return

  loading.value = true
  try {
    const res = await api.getAddresses(userStore.userInfo.id)
    if (res.code === 200) {
      addresses.value = res.data
    }
  } catch (error) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

const handleEdit = (addr) => {
  isEdit.value = true
  editId.value = addr.id
  form.receiver = addr.receiver
  form.phone = addr.phone
  form.address = addr.address
  form.isDefault = addr.is_default === 1
  showDialog.value = true
}

const handleSetDefault = async (id) => {
  try {
    const res = await api.updateAddress(id, { is_default: 1 })
    if (res.code === 200) {
      ElMessage.success('设置成功')
      loadAddresses()
    }
  } catch (error) {
    ElMessage.error(error)
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该地址吗？', '提示', { type: 'warning' })
    const res = await api.deleteAddress(id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      loadAddresses()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error)
    }
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitLoading.value = true
  try {
    const data = {
      user_id: userStore.userInfo.id,
      receiver: form.receiver,
      phone: form.phone,
      address: form.address,
      is_default: form.isDefault ? 1 : 0
    }

    let res
    if (isEdit.value) {
      res = await api.updateAddress(editId.value, data)
    } else {
      res = await api.createAddress(data)
    }

    if (res.code === 200) {
      ElMessage.success(isEdit.value ? '更新成功' : '添加成功')
      showDialog.value = false
      loadAddresses()
      resetForm()
    }
  } catch (error) {
    ElMessage.error(error)
  } finally {
    submitLoading.value = false
  }
}

const resetForm = () => {
  form.receiver = ''
  form.phone = ''
  form.address = ''
  form.isDefault = false
  isEdit.value = false
  editId.value = null
}

onMounted(() => {
  userStore.checkLogin()
  if (userStore.userInfo) {
    loadAddresses()
  }
})
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.address-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.address-info {
  flex: 1;
}

.receiver {
  font-weight: 500;
  margin-bottom: 5px;
}

.phone {
  color: #999;
  font-size: 14px;
  margin-bottom: 5px;
}

.address {
  color: #666;
}

.actions {
  display: flex;
  gap: 10px;
}
</style>
