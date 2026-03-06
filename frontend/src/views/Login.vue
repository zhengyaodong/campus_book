<template>
  <div class="login-page">
    <div class="login-card">
      <h2>登录</h2>
      <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleSubmit">
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="邮箱或手机号"
            prefix-icon="User"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="form.remember">记住密码</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit" style="width: 100%">
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <div class="footer">
        <span>还没有账号？</span>
        <router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const form = reactive({
  username: '',
  password: '',
  remember: false
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度6-20位', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const success = await userStore.login(form.username, form.password)
    if (success) {
      ElMessage.success('登录成功')
      router.push('/')
    }
  } catch (error) {
    ElMessage.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: #fff;
  padding: 40px;
  border-radius: 12px;
  width: 400px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.login-card h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.footer {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.footer a {
  color: #409eff;
  text-decoration: none;
  margin-left: 5px;
}
</style>
