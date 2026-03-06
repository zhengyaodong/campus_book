<template>
  <div class="profile-page">
    <div class="container">
      <div class="card">
        <h2>个人资料</h2>
        <el-form :model="form" label-width="80px">
          <el-form-item label="头像">
            <el-avatar :size="80">{{ form.nickname?.[0] || '?' }}</el-avatar>
          </el-form-item>
          <el-form-item label="用户名">
            <el-input v-model="form.username" disabled />
          </el-form-item>
          <el-form-item label="昵称">
            <el-input v-model="form.nickname" />
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="form.email" />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="form.phone" />
          </el-form-item>
          <el-form-item label="注册时间">
            <el-input :value="form.created_at" disabled />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="handleSubmit">保存修改</el-button>
            <el-button @click="$router.back()">返回</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const form = reactive({
  username: '',
  nickname: '',
  email: '',
  phone: '',
  created_at: ''
})

const handleSubmit = async () => {
  loading.value = true
  try {
    const success = await userStore.updateProfile({
      nickname: form.nickname,
      email: form.email,
      phone: form.phone
    })
    if (success) {
      ElMessage.success('保存成功')
    }
  } catch (error) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  userStore.checkLogin()
  if (userStore.userInfo) {
    form.username = userStore.userInfo.username
    form.nickname = userStore.userInfo.nickname
    form.email = userStore.userInfo.email
    form.phone = userStore.userInfo.phone
    form.created_at = userStore.userInfo.created_at
  } else {
    router.push('/login')
  }
})
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.card {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
}

.card h2 {
  margin-bottom: 30px;
  text-align: center;
}
</style>
